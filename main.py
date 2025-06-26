import os
import requests
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from connect import conn, encerra_conn

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = FastAPI()

@app.get("/")
def home():
    print("hello")
    return {"mensagem": "Servidor FastAPI rodando com sucesso 🚀"}
    connection = conn()
    encerra_conn(connection)

#Pegando o code do usuário pelo callback após acessa o link da twtich
@app.get("/twitch_callback", response_class=HTMLResponse)
async def twitch_callback(request: Request):
    code = request.query_params.get("code")
    print("Código de autorização recebido da Twitch:", code)

    connection = conn()
    cursor = connection.cursor()

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
            cursor.execute(
                "INSERT INTO token_twitch (token) VALUES (%s)",
                [json.dumps(token_json)]
            )
            connection.commit()
        else:
            return HTMLResponse("Erro ao autenticar: " + response.text)

        cursor.close()
        encerra_conn(connection)
        print("Resposta da Twitch:", response.json())
    except requests.exceptions.RequestException as e:
        # Erros relacionados à requisição (ex: sem conexão, timeout, URL errada)
        return HTMLResponse(f"Erro de requisição ao tentar autenticar com a Twitch: {str(e)}")

    return HTMLResponse("<h1>Autenticação concluída com sucesso! 🎉</h1>")

@app.get("/get_chatters", response_class=HTMLResponse)
async def get_chatters(request: Request):
    try:
        connection = conn()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT token FROM token_twitch ORDER BY id DESC LIMIT 1"
        )

        token = cursor.fetchone()

        if token:
            json_data = token[0]
            access_token = json_data.get("access_token")

        cursor.close()
        encerra_conn(connection)

        params = {
            "broadcaster_id" : "138603338",
            "moderator_id" : "138603338"
        }

        headers = {
            "Authorization" : "Bearer " + access_token,
            "Client-Id" : "fokrmhg7uzg90wxqn9rnl3sz0yyiou"
        }

        chatters = requests.get("https://api.twitch.tv/helix/chat/chatters", params=params, headers=headers)
        return HTMLResponse(chatters.text)
        print(chatters.json())
    except requests.exceptions.RequestException as e:
        #await refazer_token(request)
        return HTMLResponse("Erro ao autenticar, tente novamente: " + str(e))

@app.get("/get_refreshToken", response_class=HTMLResponse)
async def refazer_token(request: Request):

    try:
        connection = conn()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT token FROM token_twitch ORDER BY id DESC LIMIT 1"
        )

        refresh_token_bruto = cursor.fetchone()


        if refresh_token_bruto:
            json_data = refresh_token_bruto[0]
            refresh_token = json_data.get("refresh_token")

        data = {
            "client_id" : client_id,
            "client_secret" : client_secret,
            "refresh_token" : refresh_token,
            "grant_type" : "refresh_token"
        }
        acess_token = requests.post("https://id.twitch.tv/oauth2/token", data=data)

        if acess_token.status_code == 200:
            token_json = acess_token.json()
            json_str = json.dumps(token_json)
            cursor.execute(
                "UPDATE token_twitch SET token = %s WHERE id = (SELECT id FROM token_twitch ORDER BY id DESC LIMIT 1)",
                [json_str]
            )
            connection.commit()
            cursor.close()
            encerra_conn(connection)
            print("Resposta da Twitch deu certo:", acess_token.json())
        else:
            return HTMLResponse("Erro ao autenticar: " + acess_token.text)
            cursor.close()
            encerra_conn(connection)

    except requests.exceptions.RequestException as e:
        return HTMLResponse("Erro ao autenticar, tente novamente: " + str(e))


