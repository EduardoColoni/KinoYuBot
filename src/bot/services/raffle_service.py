import random
import asyncio

import requests
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

import uuid
import urllib.parse


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

async def raffle_loop(time_in_seconds: int, guild_id: str, user_input: bool):
    while True:
        await asyncio.sleep(time_in_seconds)

        # Verifica se ainda deve continuar (consulta banco ou flag)
        if not await can_run_func(user_input):
            break

        # Decide se haverá sorteio
        if random.choice([True, False]):
            await raffle_item_func()
        # Se False, só espera o próximo ciclo


def insert_user_configs():
    print()

def user_configs_return():
    print()

def get_raffle_id(guild_id: str):
    repo_raffle = PostgresRepositoryRaffle()
    #Vai fazer uma consulta no banco para me retornar o streamer id usando o guild_id como chave
    streamer_id = repo_raffle.get_streamer_id(guild_id)
    #Agora com o streamer_id pego vai fazer mais uma consulta para agora pegar o raffle_id usando de base o stramer_id para filtrar
    raffle_id = repo_raffle.get_last_raffle_id(streamer_id)
    return int(raffle_id), int(streamer_id)

def can_run_func(user_input: bool, guild_id: str):
    repo_raffle = PostgresRepositoryRaffle()
    raffle_id = get_raffle_id(guild_id)
    item_list_active = repo_raffle.verify_item_list(raffle_id)
    raffle_status = True
    if not user_input or not item_list_active:
        raffle_status = False
    return raffle_status

def raffle_viewer(streamer_id: int):
    url_base = api_config["URL_BASE"]
    response = requests.get(f"{url_base}/get_chatters")
    raw_viewers = response.json()
    viewers_list = raw_viewers["data"]
    winner = random.choice(viewers_list)
    return winner

def raffle_item_func(guild_id: str):
    repo_raffle = PostgresRepositoryRaffle()
    raffle_item = repo_raffle.make_raffle(guild_id)
    return raffle_item

def update_item(winner_name: str, item_id: int, raffle_id: int):
    repo_raffle = PostgresRepositoryRaffle()
    repo_raffle.update_item(winner_name, item_id, raffle_id)