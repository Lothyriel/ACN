import asyncio
from datetime import datetime
from operator import xor
import discord
from discord.utils import get

import humanize as humanize
from discord.ext import commands


def canal_voz_invalido(user):
    return not hasattr(user, 'voice') or not user.voice


async def movecao(member, member_current_voice_channel, move_channel):
    for _ in range(10):
        await member.move_to(channel=move_channel)
        await asyncio.sleep(0.10)
        await member.move_to(channel=member_current_voice_channel)
        await asyncio.sleep(0.10)


tuco_id = 186973041073455105


class Diversos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.bot.debug:
            await self.logacao(member, after, before)

        await self.movecao_arkhandinica(member, after)

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
        member: discord.Member = discord.utils.get(
            self.bot.get_all_members(), id=alvo.id)

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

    @commands.command(help="Move pessoa")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def shake2(self, ctx, alvo: discord.User):
        member: discord.Member = discord.utils.get(
            self.bot.get_all_members(), id=alvo.id)

        if self.eh_tuco(member):
            await ctx.send(f'O {ctx.author.mention} acabou de levar a invertida do TJSC...')
            member = ctx.author

        elif discord.utils.get(ctx.guild.roles, name="anti-zuck") in member.roles:
            await ctx.send(f'O {ctx.author.mention} acabou de levar a invertida anti-zuck...')
            member = ctx.author

        if canal_voz_invalido(member):
            return await ctx.send(f'O {alvo.mention} não está conectado...')

        member_current_voice_channel = member.voice.channel

        move_channel = list(filter(
            lambda x: x.id is not member_current_voice_channel.id, ctx.guild.voice_channels))[0]

        await movecao(member, member_current_voice_channel, move_channel)

    async def movecao_arkhandinica(self, member, after):
        if "rkhan" in member.discriminator and after.self_mute and after.self_stream:
            la_palomba = discord.utils.get(
                self.bot.guilds, id=244922266050232321)

            canal_movecao = la_palomba.voice_channels[1] if la_palomba.voice_channels[
                0].id == after.channel.id else la_palomba.voice_channels[0]

            await movecao(member, after.channel, canal_movecao)

    async def logacao(self, member, after, before):
        mito = await self.bot.fetch_user(self.id_pirocudo)

        if after.channel and not before.channel:
            await mito.send(f'{member} entrou')

        if not after.channel and before.channel:
            await mito.send(f'{member} saiu')

        await mito.send(f'{member} está {"mutado" if after.self_mute else "desmutado"}')
        await mito.send(f'{member} {"" if after.self_stream else "não"} está streamando')

    def eh_tuco(self, member):
        return member.id == tuco_id

    @commands.command(help="Limpar chat")
    async def clean(self, ctx, amount):

        # if self.bot.eh_plebe(ctx.author):
        #     return await ctx.send("Seu pau é infelizmente muito pequeno para utilizar este comando")
            
        amount = int(amount)

        if amount > 100:
            return await ctx.send('menos de 100 mensagens por favor...')

        # async for message in ctx.channel.history(limit = amount + 1):
        #     await message.delete()

        await ctx.channel.purge(limit = amount + 1)

        return await ctx.send(f'foram deletadas {amount} mensagens')
