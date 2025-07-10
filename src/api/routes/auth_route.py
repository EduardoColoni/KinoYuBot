from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
import requests
from src.database.postgres.postgres_repository_auth import PostgresRepository
from src.database.postgres.postgres_repository_raffle import PostgresRepositoryRaffle
from src.database.redis.redis_repository import RedisRepository
from src.database.redis.connection.redis_connection import RedisConnectionHandle
import urllib.parse
from src.core.config import twitch

router = APIRouter()


@router.get("/teste_guild/{guild}", response_class=HTMLResponse)
async def test_guild(request: Request, guild: str):
    repo_raffle = PostgresRepositoryRaffle()
    guild_id = repo_raffle.select_guild_id(guild)
    return HTMLResponse(str(guild_id))

@router.get("/twitch_callback", response_class=HTMLResponse)
async def twitch_callback(request: Request):
    redis_conn = RedisConnectionHandle().connect()
    redis_repository = RedisRepository(redis_conn)
    repo = None
    code = request.query_params.get("code")
    encoded_state = request.query_params.get("state")

    if not code or not encoded_state:
        return HTMLResponse("<h1>Erro: parâmetro ausente.</h1>", status_code=400)

    state = urllib.parse.unquote(encoded_state)
    try:
        guild_id, csrf = state.split(":")
    except:
        return HTMLResponse("<h1>State malformado.</h1>", status_code=400)

    stored_guild = redis_repository.get(f"oauth_state:{csrf}")
    if not stored_guild or stored_guild != guild_id:
        return HTMLResponse("<h1>State inválido ou expirado.</h1>", status_code=403)

    redis_repository.delete(f"oauth_state:{csrf}")

    data = {
        "client_id": twitch["CLIENT_ID"],
        "client_secret": twitch["CLIENT_SECRET"],
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": twitch["REDIRECT_URI"]
    }

    try:
        #Enviando um request de post para pegar o token e o refresh token
        response = requests.post(twitch["TWITCH_URL"] + "/token", data=data)
        #Inserindo no banco de dados a reposta do request

        if response.status_code == 200:
            token_json = response.json()

            streamer_name, streamer_id = get_user(token_json["access_token"])
            print("Resposta da Twitch:", token_json)
            repo = PostgresRepository()
            repo.insert_token(token_json, streamer_id, guild_id, streamer_name) #########################################
            #print("Resposta da Twitch:", token_json)
            return HTMLResponse("<h1>Autenticação concluída com sucesso! 🎉</h1>")
        else:
            return HTMLResponse("Erro ao autenticar: " + response.text)

    except requests.exceptions.RequestException as e:
        # Erros relacionados à requisição (ex: sem conexão, timeout, URL errada)
        return HTMLResponse(f"Erro de requisição ao tentar autenticar com a Twitch: {str(e)}")
    finally:
        if repo:  # Fecha a conexão se ela existir
            repo.close()

@router.get("/get_refreshToken", response_class=HTMLResponse)
async def refazer_token(request: Request):
    repo = None
    try:
        repo = PostgresRepository()
        token_data = repo.select_token()

        if token_data:
            refresh_token = token_data.get("refresh_token")

        data = {
            "client_id": twitch["CLIENT_ID"],
            "client_secret": twitch["CLIENT_SECRET"],
            "refresh_token" : refresh_token,
            "grant_type" : "refresh_token"
        }
        access_token = requests.post(f"{twitch['TWITCH_URL']}/token", data=data)

        if access_token.status_code == 200:
            token_json = access_token.json()

            repo.refresh_token(token_json)

            print("Resposta da Twitch deu certo:", access_token.json())
        else:
            return HTMLResponse("Erro ao autenticar: " + access_token.text)

    except requests.exceptions.RequestException as e:
        return HTMLResponse("Erro ao autenticar, tente novamente: " + str(e))

    finally:
        if repo:  # Fecha a conexão se ela existir
            repo.close()


def get_user(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-Id": twitch["CLIENT_ID"]
    }

    response = requests.get("https://api.twitch.tv/helix/users", headers=headers)
    response.raise_for_status()

    data = response.json()
    user = data["data"][0]
    return user["login"], user["id"]
