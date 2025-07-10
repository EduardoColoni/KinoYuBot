import requests
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from src.database.postgres.postgres_repository_auth import PostgresRepository
from src.core.config import twitch
router = APIRouter()

@router.get("/get_chatters", response_class=HTMLResponse)
async def get_chatters(request: Request):
    repo = None
    try:

        repo = PostgresRepository()
        token_data = repo.select_token()

        if not token_data or "access_token" not in token_data:
            return HTMLResponse("Token de acesso não encontrado.")

        access_token = token_data["access_token"]

        params = {
            "broadcaster_id" : "46736025",
            "moderator_id" : "46736025"
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "client_id": twitch["CLIENT_ID"]
        }

        chatters = requests.get("https://api.twitch.tv/helix/chat/chatters", params=params, headers=headers)
        return HTMLResponse(chatters.text)

        print(chatters.json())

    except requests.exceptions.RequestException as e:
        #await refazer_token(request)
        return HTMLResponse("Erro ao autenticar, tente novamente: " + str(e))

    finally:
        if repo:  # Fecha a conexão se ela existir
            repo.close()

@router.get("/ola", response_class=HTMLResponse)
async def ola(request: Request, guild: str):
    headers = {
        "Authorization": f"Bearer i4o011nqlh9wp8p4k6whs5syfac0us",
        "client_id": twitch["CLIENT_ID"]
    }
    streamer_response = requests.get("https://api.twitch.tv/helix/users", headers=headers)

    data = streamer_response.json()
    streamer_name = data["data"][0]["login"]
    streamer_id = data["data"][0]["id"]



    return print(streamer_id, streamer_name)
