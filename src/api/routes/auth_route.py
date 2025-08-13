from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
import requests
import urllib.parse

from src.core.config import twitch
from src.database.postgres.postgres_repository_auth import PostgresRepositoryAuth
from src.database.postgres.connection.postgres_connection import PostgresPool
from src.database.redis.redis_repository import RedisRepository
from src.database.redis.connection.redis_connection import RedisConnectionHandle


class TwitchAuthController:
    def __init__(self):
        self.redis_conn = RedisConnectionHandle().connect()
        self.router = APIRouter()
        self.router.add_api_route("/twitch_callback", self.twitch_callback, methods=["GET"])
        self.router.add_api_route("/get_refreshToken", self.refresh_token, methods=["GET"])

    async def twitch_callback(self, request: Request):
        redis_repo = RedisRepository(self.redis_conn)
        conn = PostgresPool.get_conn()
        try:
            repo_auth = PostgresRepositoryAuth(conn)

            code = request.query_params.get("code")
            encoded_state = request.query_params.get("state")

            if not code or not encoded_state:
                return HTMLResponse("<h1>Erro: parâmetro ausente.</h1>", status_code=400)

            state = urllib.parse.unquote(encoded_state)
            guild_id, csrf = state.split(":")

            stored_guild = redis_repo.get(f"oauth_state:{csrf}")
            if not stored_guild or stored_guild != guild_id:
                return HTMLResponse("<h1>State inválido ou expirado.</h1>", status_code=403)

            redis_repo.delete(f"oauth_state:{csrf}")

            data = {
                "client_id": twitch["CLIENT_ID"],
                "client_secret": twitch["CLIENT_SECRET"],
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": twitch["REDIRECT_URI"]
            }

            response = requests.post(twitch["TWITCH_URL"] + "/token", data=data, timeout=10)

            if response.status_code == 200:
                token_json = response.json()
                streamer_name, streamer_id = self._get_user(token_json["access_token"])
                repo_auth.insert_token(token_json, streamer_id, guild_id, streamer_name)
                print("Autenticação concluída com sucesso!")
                return HTMLResponse("<h1>Autenticação concluída com sucesso! 🎉</h1>")

            return HTMLResponse(f"Erro ao autenticar: {response.text}", status_code=response.status_code)

        except ValueError:
            return HTMLResponse("<h1>State malformado.</h1>", status_code=400)
        except requests.exceptions.RequestException as e:
            return HTMLResponse(f"<h1>Erro de requisição: {str(e)}</h1>", status_code=500)
        finally:
            PostgresPool.release_conn(conn)

    async def refresh_token(self, request: Request):
        conn = PostgresPool.get_conn()
        try:
            repo_auth = PostgresRepositoryAuth(conn)

            token_data = repo_auth.select_token()
            if not token_data:
                return HTMLResponse("<h1>Token não encontrado.</h1>", status_code=401)

            refresh_token = token_data.get("refresh_token")
            if not refresh_token:
                return HTMLResponse("<h1>Refresh token ausente.</h1>", status_code=400)

            data = {
                "client_id": twitch["CLIENT_ID"],
                "client_secret": twitch["CLIENT_SECRET"],
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
                "redirect_uri": twitch["REDIRECT_URI"]
            }

            response = requests.post(f"{twitch['TWITCH_URL']}/token", data=data, timeout=10)

            if response.status_code == 200:
                token_json = response.json()
                repo_auth.refresh_token(token_json)
                print("Token atualizado com sucesso!")
                return HTMLResponse("<h1>Token atualizado com sucesso!</h1>")

            return HTMLResponse(f"Erro ao atualizar token: {response.text}", status_code=response.status_code)

        except requests.exceptions.RequestException as e:
            return HTMLResponse(f"<h1>Erro na requisição: {str(e)}</h1>", status_code=500)
        finally:
            PostgresPool.release_conn(conn)

    def _get_user(self, token: str):
        headers = {
            "Authorization": f"Bearer {token}",
            "Client-Id": twitch["CLIENT_ID"]
        }

        response = requests.get("https://api.twitch.tv/helix/users", headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        user = data["data"][0]
        return user["login"], user["id"]


def setup_auth_routes():
    controller = TwitchAuthController()
    return controller.router
