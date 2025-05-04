import psycopg2 as pg
from psycopg2 import Error
from dotenv import load_dotenv
import os

load_dotenv()

def conn():
    try:
        pwd = os.getenv("DB_PASSWORD")
        conecta = pg.connect(
            user="postgres",
            password=pwd,
            host="localhost",
            port=5432,
            database="twitch_autenticacao"
        )
        print("Conectado com sucesso!")
        return conecta

    except Error as e:
        print(f"[ERRO BANCO] Falha ao conectar ao banco de dados: {e}")
        # Aqui lançamos o erro para quem chamou a função tratar
        raise RuntimeError("Erro ao conectar ao banco de dados") from e

def encerra_conn(conecta):
    if conecta:
        conecta.close()
