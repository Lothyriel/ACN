import os

import discord
from discord.ext import commands

class EnviaSojado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Envia N sojados.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def soja(self, ctx) -> None:

        path = os.getcwd() + "/images/"        
        for pathSojado in os.listdir(path):
            with open(path + pathSojado, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
        
