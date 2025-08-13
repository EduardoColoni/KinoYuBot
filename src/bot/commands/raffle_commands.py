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

from src.bot.services.raffle_service import RaffleService
from src.database.postgres.connection.postgres_connection import PostgresPool
from src.database.redis.redis_repository import RedisRepository
from src.database.redis.connection.redis_connection import RedisConnectionHandle
from src.database.postgres.postgres_repository_raffle import PostgresRepositoryRaffle

from src.bot.services import raffle_service

import uuid
import urllib.parse

# Classe do Modal que coleta os itens do sorteio
class RegisterRaffleModal(discord.ui.Modal, title="Registrar itens para sorteio"):
    def __init__(self):
        super().__init__(title="Registrar itens")
    itens = discord.ui.TextInput(label="Adicione itens(item1:peso1, item2:peso2, etc)", placeholder="ex: skin dourada:50, skin prata:30", max_length=100, style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        conn = PostgresPool.get_conn()
        try:
            guild_id = str(interaction.guild.id)
            repo_raffle = PostgresRepositoryRaffle(conn)  # passa a conexão
            service = RaffleService(conn, guild_id)
            raffle_id = repo_raffle.make_raffle_id(guild_id)
            itens_bruto = self.itens.value
            itens_processados = service.organizar_itens(itens_bruto)

            for item, peso in itens_processados:
                repo_raffle.insert_items(item=item, weight=peso, raffle_id=raffle_id, guild_id=guild_id)

            await interaction.response.send_message("Itens registrados com sucesso!")

        except Exception as e:
            service = RaffleService()
            erro = service.organizar_itens()
            await interaction.response.send_message(f"Erro ao inserir os itens, tente novamente e verifique se a formatação está correta!\nErro: {erro}")
            conn.rollback()
            raise RuntimeError(f"Erro ao inserir itens: {e}")
        finally:
            PostgresPool.release_conn(conn)

# Cog com os comandos do bot
class Raffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.service = None  # vai guardar a instância do service

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

    @app_commands.command()
    async def iniciar_sorteio(self, interaction: discord.Interaction):
        if not self.service:
            conn = PostgresPool.get_conn()
            try:
                guild_id = str(interaction.guild.id)
                self.service = RaffleService(conn, guild_id)

                await interaction.response.send_message("Iniciando sorteio...")

                # Função callback que será chamada pelo raffle_loop
                async def notify_winner(winner_name, item = None):
                    if not winner_name:
                        await interaction.followup.send("Itens para sorteio vazio ou usuário parou a função")
                        return
                    else:
                        await interaction.followup.send(f"🎉 O vencedor foi **{winner_name}** com o item {item}!")

                # Passa o callback para o raffle_loop
                await self.service.raffle_loop(5, notify_winner)
                self.service = None

            finally:
                PostgresPool.release_conn(conn)
        else:
            await interaction.response.send_message("Sorteio já em execução.")

    @app_commands.command()
    async def parar(self, interaction: discord.Interaction):
        if self.service:
            self.service.user_input = False
            await interaction.response.send_message("Sorteio parado!")
        else:
            await interaction.response.send_message("Nenhum sorteio em execução.")

# Setup para carregar o Cog
async def setup(bot):
    await bot.add_cog(Raffle(bot))

