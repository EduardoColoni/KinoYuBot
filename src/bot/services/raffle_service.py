import random
import asyncio
import re
from functools import partial

import requests
from anyio import sleep
from src.core.config import api_config

from src.database.redis.redis_repository import RedisRepository
from src.database.redis.connection.redis_connection import RedisConnectionHandle
from src.database.postgres.postgres_repository_raffle import PostgresRepositoryRaffle
from src.database.postgres.connection.postgres_connection import PostgresPool

class RaffleService:
    def __init__(self, conn=None, guild_id=None):
        self.guild_id = guild_id
        self.conn = conn
        self.repo_raffle = PostgresRepositoryRaffle(self.conn)
        self.user_input = True

    async def raffle_loop(self, time_in_seconds: int, on_winner_callback):
        while True:
            await asyncio.sleep(time_in_seconds)

            item = await asyncio.to_thread(partial(self.repo_raffle.make_raffle, self.guild_id))
            if not self.user_input or not item:
                await on_winner_callback(None)
                print("Itens para sorteio vazio ou usuário parou a função")
                break

            if random.choice([True, False]):
                viewer = await asyncio.to_thread(partial(self.raffle_viewer, item[2]))
                winner_name = str(viewer["user_name"])
                streamer_id = str(item[2])
                item_name = str(item[3])
                self.update_item(winner_name, item[0], item[1])
                print(f"Sorteio feito: {item}, vencedor: {viewer}")
                url_base = api_config["URL_BASE"]
                response = requests.post(f"{url_base}/send_message/{streamer_id}/{winner_name}/{item_name}")

                # Chama o callback e passa as informações
                await on_winner_callback(winner_name, item)

            else:
                print("Não haverá sorteio nesse turno")

    @staticmethod
    def raffle_viewer(platform_id: int):
        url_base = api_config["URL_BASE"]

        def get_chatters():
            resp = requests.get(f"{url_base}/get_chatters/{platform_id}")
            if resp.status_code != 200:
                raise RuntimeError(f"Erro ao buscar chatters: {resp.status_code} - {resp.text}")
            try:
                return resp.json()
            except ValueError as e:
                raise RuntimeError(f"Resposta não é JSON: {e}")

        try:
            raw_viewers = get_chatters()
        except RuntimeError:
            # Tentativa de refresh
            refresh_resp = requests.get(f"{url_base}/get_refreshToken")
            if refresh_resp.status_code != 200:
                raise RuntimeError(f"Falha ao renovar token: {refresh_resp.status_code} - {refresh_resp.text}")
            # Tentativa novamente após refresh
            raw_viewers = get_chatters()

        viewers_list = raw_viewers.get("data", [])
        if not viewers_list:
            raise RuntimeError("Nenhum viewer retornado.")

        return random.choice(viewers_list)

    def update_item(self, winner_name: str, item_id: int, raffle_id: int):
        try:
            self.repo_raffle.update_item(winner_name, item_id, raffle_id)
        except Exception as e:
            self.conn.rollback()
            print(f"Falha ao atualizar o item: {item_id} erro: {e}")

    @staticmethod
    def organizar_itens(itens = None):
        try:
            pares = itens.split(",")
            itens_processados = []

            for par in pares:
                par = par.strip()
                if not par:
                    continue

                # Se tiver delimitador, pega nome e peso
                if ":" in par or ";" in par:
                    nome, peso = re.split("[:;]", par, maxsplit=1)
                    nome = nome.strip()
                    peso = peso.strip()
                    # Se peso não for numérico, ignora ou define None
                    peso_valor = int(peso) if peso.isdigit() else None
                    if not nome:
                        continue
                    itens_processados.append((nome, peso_valor))
                else:
                    return

            return itens_processados
        except:
            return("Item não foram dividos por virgula")