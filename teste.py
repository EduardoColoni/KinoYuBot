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

connection = conn()


cursor = connection.cursor()

cursor.execute(
            "SELECT json_token FROM token_twitch"
        )
token = cursor.fetchone()

json_token = token[0]
refresh_token = json_token['refresh_token']

dataOld = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "refresh_token",
    "refresh_token": refresh_token
}

response = requests.post("https://id.twitch.tv/oauth2/token", data=dataOld)

newcode = response.json()

print(newcode)

encerra_conn(connection)