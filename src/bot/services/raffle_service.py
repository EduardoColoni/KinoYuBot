import random
import asyncio
from functools import partial

import requests
from aiohttp import streamer
from anyio import sleep
from discord import app_commands
from discord.ext import commands, tasks
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from watchgod import awatch

from src.core.config import api_config

from src.database.redis.redis_repository import RedisRepository
from src.database.redis.connection.redis_connection import RedisConnectionHandle
from src.database.postgres.postgres_repository_raffle import PostgresRepositoryRaffle
from src.database.postgres.connection.postgres_connection import PostgresPool
import uuid
import urllib.parse


class RaffleService:
    def __init__(self, conn, guild_id: str):
        self.guild_id = guild_id
        self.conn = conn
        self.repo_raffle = PostgresRepositoryRaffle(self.conn)

    @staticmethod
    def organizar_itens(itens):
        pares = itens.split(",")

        # Lista para guardar os itens formatados
        itens_processados = []

        for par in pares:
            # Quebra cada item pelo dois-pontos
            if ":" not in par:
                continue  # pula se não tiver formato esperado

            nome, peso = par.split(":", 1)  # 1 = no máximo uma divisão

            nome = nome.strip()
            peso = peso.strip()

            if not nome or not peso.isdigit():
                continue  # ignora se algo estiver errado

            itens_processados.append((nome, int(peso)))

        return itens_processados

    async def raffle_loop(self, time_in_seconds: int, user_input: bool):
        while True:
            await asyncio.sleep(time_in_seconds)

            item = await asyncio.to_thread(partial(self.repo_raffle.make_raffle, self.guild_id))
            if not user_input or not item:
                print("Itens para sorteio vazio ou usuário parou a função")
                break

            if random.choice([True, False]):
                viewer = await asyncio.to_thread(partial(self.raffle_viewer, item[2]))
                winner_name = str(viewer["user_name"])
                self.update_item(winner_name, item[0], item[1])
                print(f"Sorteio feito: {item}, vencedor: {viewer}")
            else:
                print("Não haverá sorteio nesse turno")

    @staticmethod
    def raffle_viewer(platform_id: int):
        url_base = api_config["URL_BASE"]
        response = requests.get(f"{url_base}/get_chatters/{platform_id}")
        if response.status_code != 200:
            raise RuntimeError(f"Erro ao buscar chatters: {response.status_code} - {response.text}")

        try:
            raw_viewers = response.json()
        except ValueError as e:
            raise RuntimeError(f"Resposta não é JSON: {e}")
        viewers_list = raw_viewers["data"]
        winner = random.choice(viewers_list)
        return winner

    def update_item(self, winner_name: str, item_id: int, raffle_id: int):
        try:
            self.repo_raffle.update_item(winner_name, item_id, raffle_id)
        except Exception as e:
            self.conn.rollback()
            print(f"Falha ao atualizar o item: {item_id} erro: {e}")