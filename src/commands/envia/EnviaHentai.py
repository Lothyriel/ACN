import asyncio
import typing
from json import JSONDecodeError
from random import randrange

import discord
import requests
from discord.ext import commands

async def get_request_hentai(url):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, requests.get, url)
    try:
        posts = response.json()
        return posts
    except JSONDecodeError:
        if len(response.content) == 0:
            return [{"file_url": "Tag não encontrada"}]
        return [{"file_url": "Erro na Request"}]


class EnviaHentai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Use com precaução <user=opcional> <tag=opcional>")
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def spam(self, ctx, alvo: typing.Optional[discord.User], *tag):
        await asyncio.gather(*[self.hentai(ctx, alvo, *tag) for _ in range(1, 15)])

    @commands.command(help="<user=opcional> <tag=opcional>")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hentai(self, ctx, alvo: typing.Optional[discord.User], *tag):
        if len(tag) == 0:
            posts = await get_request_hentai('https://rule34.xxx//index.php?page=dapi&json=1&s=post&id={}&q=index'.format(str(randrange(1, 4555950))))
            url = posts[0]["file_url"]
        else:
            tag = "_".join(tag)
            posts = await get_request_hentai('https://rule34.xxx/index.php?page=dapi&json=1&s=post&tags={}&q=index'.format(tag))
            url = posts[randrange(0, len(posts))]["file_url"]

        if "Erro" not in url:
            return await alvo.send(url) if alvo else await ctx.send(url)
