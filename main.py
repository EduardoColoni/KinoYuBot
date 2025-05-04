import os
import requests
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from connect import conn, encerra_conn

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

app = FastAPI()

@app.get("/")
def home():
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
                "INSERT INTO token_twitch (json_token) VALUES (%s)",
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
    except requests.exceptions.RequestException as e:
        # Erros relacionados à requisição (ex: sem conexão, timeout, URL errada)
        return HTMLResponse(f"Erro de requisição ao tentar autenticar com a Twitch: {str(e)}")

    return HTMLResponse("<h1>Autenticação concluída com sucesso! 🎉</h1>")
