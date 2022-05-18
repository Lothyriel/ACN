import asyncio
import os
import typing
from json import JSONDecodeError
from random import randrange

import discord
import requests
from discord.ext import commands

class EnviaSojado(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Envia N sojados.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def soja(self, ctx):

        path = os.getcwd() + "/images/"
        for pathSojado in path:
            with open(pathSojado, 'rb') as f:
                picture = discord.File(f)
                await ctx.send(file=picture)
        
