import discord
from discord.ext import commands
from src.core.config import discord_config

intents = discord.Intents.all()

bot = commands.Bot("!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Comandos de barra sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

# Carrega os comandos de outro arquivo
async def load():
    await bot.load_extension("src.bot.commands.raffle_commands")

# Executa o carregamento e inicia o bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(load())
    bot.run(discord_config['TOKEN'])