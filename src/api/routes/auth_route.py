from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
import requests
from src.database.postgres.postgres_repository import PostgresRepository
from src.core.config import twitch

router = APIRouter()

@router.get("/twitch_callback", response_class=HTMLResponse)
async def twitch_callback(request: Request):
    repo = None
    code = request.query_params.get("code")
    print("Código de autorização recebido da Twitch:", code)

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
            repo = PostgresRepository()
            repo.insert_token(token_json)
            print("Resposta da Twitch:", token_json)
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