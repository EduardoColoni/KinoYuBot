import requests
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from src.database.postgres.postgres_repository import PostgresRepository

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
            "broadcaster_id" : "102089057",
            "moderator_id" : "102089057"
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-Id": "fokrmhg7uzg90wxqn9rnl3sz0yyiou"
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