from datetime import datetime

import humanize as humanize
from discord.ext import commands


class Diversos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Mandar <msg> para todos os grupos")
    async def att(self, ctx, *msg):
        if self.bot.eh_plebe(ctx.author):
            return await ctx.send("Seu pau é infelizmente muito pequeno para utilizar este comando")

        mensagem = " ".join(msg)
        for grupo in self.bot.guilds:
            await grupo.text_channels[0].send(mensagem)

    @commands.command(help="Indica a quanto tempo estou vivo", aliases=["vivo"])
    async def alive(self, ctx):
        await ctx.send("Estou sem bugar desde {}".format(humanize.naturaltime(datetime.now() - self.bot.iniciei)))
