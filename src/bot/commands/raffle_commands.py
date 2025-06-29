import discord
from discord.ext import commands
from ..services.raffle_service import sorteio

intents = discord.Intents.all()

@commands.command()
async def raffle_commands(interact:discord.Interaction, skin, peso):
    sorteio(skin, peso)
    await interact.response.send_message(sorteio)