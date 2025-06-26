import discord
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
token = os.getenv("DISCORD_TOKEN")

if not token:
    raise ValueError("Token não encontrado! Verifique o arquivo .env")


intents = discord.Intents.all()
bot = commands.Bot("!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")


@bot.command()
async def iniciar(ctx:commands.Context):
        await ctx.reply("O sorteio foi iniciado!")
        response = requests.get("https://remarkably-knowing-serval.ngrok-free.app/get_chatters")
        await ctx.reply(response.text)


try:
    bot.run(token)
except discord.LoginFailure:
    print("Token inválido! Verifique o .env")