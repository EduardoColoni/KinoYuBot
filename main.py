import os
import requests
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from models.postgres.postgres_repository import PostgresRepository

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = FastAPI()

@app.get("/")
def home():
    print("hello")
    return {"mensagem": "Servidor FastAPI rodando com sucesso 🚀"}

#Pegando o code do usuário pelo callback após acessa o link da twtich
@app.get("/twitch_callback", response_class=HTMLResponse)
async def twitch_callback(request: Request):
    repo = None
    code = request.query_params.get("code")
    print("Código de autorização recebido da Twitch:", code)

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code":code,
        "redirect_uri": "https://remarkably-knowing-serval.ngrok-free.app/twitch_callback"
    }

    try:
        #Enviando um request de post para pegar o token e o refresh token
        response = requests.post("https://id.twitch.tv/oauth2/token", data=data)
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

@app.get("/get_chatters", response_class=HTMLResponse)
async def get_chatters(request: Request):
    repo = None
    try:

        repo = PostgresRepository()
        token_data = repo.select_token()

        if not token_data or "access_token" not in token_data:
            return HTMLResponse("Token de acesso não encontrado.")

        access_token = token_data["access_token"]

        params = {
            "broadcaster_id" : "138603338",
            "moderator_id" : "138603338"
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

@app.get("/get_refreshToken", response_class=HTMLResponse)
async def refazer_token(request: Request):
    repo = None
    try:
        repo = PostgresRepository()
        token_data = repo.select_token()

        if token_data:
            refresh_token = token_data.get("refresh_token")

        data = {
            "client_id" : client_id,
            "client_secret" : client_secret,
            "refresh_token" : refresh_token,
            "grant_type" : "refresh_token"
        }
        acess_token = requests.post("https://id.twitch.tv/oauth2/token", data=data)

        if acess_token.status_code == 200:
            token_json = acess_token.json()

            repo.refresh_token(token_json)

            print("Resposta da Twitch deu certo:", acess_token.json())
        else:
            return HTMLResponse("Erro ao autenticar: " + acess_token.text)

    except requests.exceptions.RequestException as e:
        return HTMLResponse("Erro ao autenticar, tente novamente: " + str(e))

    finally:
        if repo:  # Fecha a conexão se ela existir
            repo.close()


