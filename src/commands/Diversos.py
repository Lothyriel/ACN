import asyncio
from datetime import datetime
from operator import xor
import discord
from discord.utils import get

import humanize as humanize
from discord.ext import commands

def canal_voz_invalido(user):
    return not hasattr(user, 'voice') or not user.voice

tuco_id = 186973041073455105
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

    @commands.command(help="Debugzinho")
    async def debug(self, ctx):
        if self.bot.eh_plebe(ctx.author):
            return await ctx.send("Seu pau é infelizmente muito pequeno para utilizar este comando")

        self.bot.debug = xor(self.bot.debug, True)
        await ctx.send("O modo Debug está {}".format("Ligado" if self.bot.debug else "Desligado"))

    @commands.command(help="Move pessoa")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def shake(self, ctx, alvo: discord.User):
        member: discord.Member = discord.utils.get(self.bot.get_all_members(), id=alvo.id)

        if self.eh_tuco(member):
            await ctx.send(f'O {ctx.author.mention} acabou de levar a invertida do TJSC...')
            member = ctx.author

        elif discord.utils.get(ctx.guild.roles, name="anti-zuck") in member.roles:
           await ctx.send(f'O {ctx.author.mention} acabou de levar a invertida anti-zuck...')
           member = ctx.author

        if canal_voz_invalido(member):
            return await ctx.send(f'O {alvo.mention} não está conectado...')

        memberCurrentVoiceChannel = member.voice.channel
        channels = ctx.guild.voice_channels        
        
        for channel in channels:
            await member.move_to(channel=channel)
            await asyncio.sleep(0.25)

        await member.move_to(channel=memberCurrentVoiceChannel)

    def eh_tuco(self, member):
        return member.id == tuco_id
