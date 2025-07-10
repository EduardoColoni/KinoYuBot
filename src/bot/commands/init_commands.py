# import discord
# from discord import app_commands
# from discord.ext import commands
# from src.bot.services.raffle_service import sorteio
#
# class Raffle(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     @app_commands.command()
#     async def ola(self, interaction: discord.Interaction):
#         await interaction.response.send_message(f"Olá, {interaction.user.name}!", ephemeral=True)
#
#
#
#     @app_commands.command(name="sorteio", description="Faz um sorteio de skin com peso")
#     @app_commands.describe(skin="Lista de skins e pesos separados por vírgula", peso="Pesos separados por vírgula")
#     async def sorteio_slash(self, interaction: discord.Interaction, skin:str, peso:str):
#         skins = skin.split(",")
#         pesos = list(map(int, peso.split(",")))
#         resultado = sorteio(skins, pesos)
#         await interaction.response.send_message(f"Item sorteado: {resultado[0]}")
#
#
# async def setup(bot):
#         await bot.add_cog(Raffle(bot))