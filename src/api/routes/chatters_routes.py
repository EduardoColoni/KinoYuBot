import requests
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from src.database.postgres.postgres_repository_auth import PostgresRepositoryAuth
from src.database.postgres.connection.postgres_connection import PostgresPool
from src.core.config import twitch


class TwitchChattersController:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            "/get_chatters/{streamer_id}",
            self.get_chatters,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/send_message/{streamer_id}/{user_id}/{item_name}",
            self.send_message,
            methods=["POST"]
        )

    async def get_chatters(self, request: Request, streamer_id: str):
        """Endpoint para obter os chatters de um canal da Twitch"""
        conn = PostgresPool.get_conn()
        try:
            repo_auth = PostgresRepositoryAuth(conn)

            token_data = repo_auth.select_token_by_streamer(streamer_id)
            if not token_data or "access_token" not in token_data:
                return HTMLResponse(
                    content="<h1>Token de acesso não encontrado</h1>",
                    status_code=401
                )

            headers = {
                "Authorization": f"Bearer {token_data['access_token']}",
                "Client-Id": twitch["CLIENT_ID"]
            }

            params = {
                "broadcaster_id": streamer_id,
                "moderator_id": streamer_id,
                "first": 1000
            }

            response = requests.get(
                "https://api.twitch.tv/helix/chat/chatters",
                headers=headers,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                print("Chatters pego com sucesso")
                return JSONResponse(content=response.json())
            return HTMLResponse(
                content=f"<h1>Erro na API Twitch: {response.text}</h1>",
                status_code=response.status_code
            )

        except requests.exceptions.RequestException as e:
            return HTMLResponse(
                content=f"<h1>Erro na requisição: {str(e)}</h1>",
                status_code=500
            )
        finally:
            PostgresPool.release_conn(conn)

    async def send_message(self, request: Request, streamer_id: str, user_id: str, item_name : str):
        conn = PostgresPool.get_conn()
        try:
            repo_auth = PostgresRepositoryAuth(conn)

            token_data = repo_auth.select_token_by_streamer("1355737213")
            if not token_data or "access_token" not in token_data:
                return HTMLResponse(
                    content="<h1>Token de acesso não encontrado</h1>",
                    status_code=401
                )

            headers = {
                "Authorization": f"Bearer {token_data['access_token']}",
                "Client-Id": twitch["CLIENT_ID"]
            }

            json_body = {
                "broadcaster_id": streamer_id,
                "moderator_id": "1355737213",
                "sender_id": "1355737213",
                "message": f"Parabéns @{user_id} você foi sorteado! e ganhou o item: {item_name}"
            }

            response = requests.post(
                "https://api.twitch.tv/helix/chat/messages",
                headers=headers,
                json=json_body
            )

            if response.status_code == 200:
                print("Mensagem enviada com sucesso")
                return JSONResponse(content=response.json())
            return HTMLResponse(
                content=f"<h1>Erro na API Twitch: {response.text}</h1>",
                status_code=response.status_code
            )

        except requests.exceptions.RequestException as e:
            return HTMLResponse(
                content=f"<h1>Erro na requisição: {str(e)}</h1>",
                status_code=500
            )
        finally:
            PostgresPool.release_conn(conn)

def setup_chatters_routes():
    controller = TwitchChattersController()
    return controller.router
