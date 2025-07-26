import random

import discord
import asyncio

import requests
from anyio import sleep
from discord import app_commands
from discord.ext import commands, tasks
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from watchgod import awatch

from src.database.redis.redis_repository import RedisRepository
from src.database.redis.connection.redis_connection import RedisConnectionHandle
from src.database.postgres.postgres_repository_raffle import PostgresRepositoryRaffle

import uuid
import urllib.parse


# Classe do Modal que coleta os itens do sorteio
class RegisterRaffleModal(discord.ui.Modal, title="Registrar itens para sorteio"):
    def __init__(self):
        super().__init__(title="Registrar itens")
    itens = discord.ui.TextInput(label="Adicione itens(item1:peso1, item2:peso2, etc)", placeholder="ex: skin dourada:50, skin prata:30", max_length=30, style=discord.TextStyle.long)
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Itens registrados com sucesso!")
        repo_raffle = PostgresRepositoryRaffle()
        guild_id = str(interaction.guild.id)
        raffle_id = repo_raffle.make_raffle_id(guild_id)
        itens_bruto = self.itens.value
        itens_processados = organizar_itens(itens_bruto)
        for item, peso in itens_processados:
            repo_raffle.insert_items(item=item, weight=peso, raffle_id = raffle_id, guild_id = guild_id)
        repo_raffle.close()

# Cog com os comandos do bot
class Raffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="iniciar", description="Inicia o processo de autenticação com a plataforma de streaming")
    async def ola(self, interaction: discord.Interaction):
        redis_conn = RedisConnectionHandle().connect()
        redis_repository = RedisRepository(redis_conn)

        guild_id = str(interaction.guild.id)
        csrf = str(uuid.uuid4())
        state = f"{guild_id}:{csrf}"
        encoded_state = urllib.parse.quote_plus(state)

        redis_repository.insert_ex(f"oauth_state:{csrf}", guild_id, 300)

        auth_url = (
            "https://id.twitch.tv/oauth2/authorize?"
            "response_type=code&"
            "client_id=fokrmhg7uzg90wxqn9rnl3sz0yyiou&"
            "redirect_uri=https%3A%2F%2Fremarkably-knowing-serval.ngrok-free.app%2Ftwitch_callback&"
            "scope=moderator%3Aread%3Achatters&"
            f"state={encoded_state}"
        )

        await interaction.response.send_message(
            f"Olá, {interaction.user.name}, clique para autenticar: {auth_url}",
            ephemeral=True
        )

    @app_commands.command(name="registrar_sorteio", description="Abre uma janela para registrar os itens do sorteio")
    async def registrar_sorteio(self, interaction: discord.Interaction):
        await interaction.response.send_modal(RegisterRaffleModal())

# Setup para carregar o Cog
async def setup(bot):
    await bot.add_cog(Raffle(bot))


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

async def raffle_loop(time_in_seconds: int, raffle_func, can_run_func):
    while True:
        await asyncio.sleep(time_in_seconds)

        # Verifica se ainda deve continuar (consulta banco ou flag)
        if not await can_run_func():
            break

        # Decide se haverá sorteio
        if random.choice([True, False]):
            await raffle_func()
        # Se False, só espera o próximo ciclo


def insert_user_configs():
    print()

def user_configs_return():
    print()

def can_run_func(user_input: bool, raffle_id: int):
    repo_raffle = PostgresRepositoryRaffle()
    item_list_active = repo_raffle.verify_item_list(raffle_id)
    raffle_status = True

    if not (item_list_active >= 0 or user_input):
        raffle_status = False

    return raffle_status

def raffle_viewer():
    response = requests.get("/get_chatters")

def raffle_func(guild_id: str):
    repo_raffle = PostgresRepositoryRaffle()
    raffle_item = repo_raffle.make_raffle(guild_id)

    print()
