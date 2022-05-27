import asyncio
import os
import typing
import random

import discord
from operator import xor
from discord.ext import commands
from pytube import Playlist
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from src.music.Musica import Musica
from src.Diversos import canal_voz_invalido

async def get_resultados(pesquisa):
    pesquisa = " ".join(pesquisa)

    path = os.getcwd() + "/music/" + pesquisa             # PEGAR OS ARQUIVOS
    if os.path.isfile(path):
        return [Musica(pesquisa, pesquisa, True)]

    if "list=" in pesquisa:
        return get_dados_playlist(pesquisa)
    if "www.youtube.com/watch?v=" in pesquisa:
        return [Musica(None, pesquisa)]

    return [await get_busca(pesquisa)]


def get_dados_playlist(pesquisa):
    return Playlist(pesquisa).video_urls


async def get_busca(pesquisa):
    loop = asyncio.get_event_loop()
    resultados = await loop.run_in_executor(None, VideosSearch, pesquisa, 1)
    resultado = resultados.result()["result"][0]
    return Musica(resultado["title"], resultado["link"])


async def get_dados_musica(musica: Musica):
    loop = asyncio.get_event_loop()
    try:
        dados = await loop.run_in_executor(None, get_dados, musica.url)
        musica.audio = dados["url"]
        if not musica.titulo:
            musica.titulo = dados["title"]
    except Exception as e:
        musica.audio = e
        return


def get_dados(url):
    ydl_opts = {'format': 'bestaudio',
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -age_limit 90'}
    with YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url=url, download=False)


class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repeatPlaylist = False
        self.fila = {}

    def load(self):
        self.fila = {guild.id: list() for guild in self.bot.guilds}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.id == self.bot.user.id:
            return

        if before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                if self.bot.debug:
                    cuzudo = await self.bot.fetch_user(self.bot.id_pirocudo)
                    await cuzudo.send(f'Timout timer {time}')
                time = time + 1
                if voice.is_playing():
                    time = 0
                if time == 600:
                    await voice.disconnect()
                    await ctx.send("Negros, estou dando a foda fora!!!")
                if not voice.is_connected():
                    break
    
    @commands.command(help="Liga o modo repeat do tocador de musica", aliases=["r"])
    async def repeat(self, ctx):
        self.repeatPlaylist = xor(self.repeatPlaylist, True)
    
    @commands.command(help="Embaralha a queue", aliases=["shuff", "sh"])
    async def shuffle(self, ctx):
        user = ctx.author

        if canal_voz_invalido(user):
            return await ctx.send("{} Repete não te escuitei".format(user.mention))

        voice_client = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)

        if not voice_client:
            await user.voice.channel.connect()

        if len(self.fila[ctx.guild.id]) != 0:
            random.shuffle(self.fila[ctx.guild.id])

        await ctx.send("Playlist embaralhada!")

    @commands.command(help="Toca musica por pesquisa ou por link <prioridade>", aliases=["p"])
    async def play(self, ctx, prioridade: typing.Optional[int] = 2, *url):
        user = ctx.author

        if canal_voz_invalido(user):
            return await ctx.send("{} Repete não te escuitei".format(user.mention))

        voice_client = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            voice_client = await user.voice.channel.connect()

        resultados = await get_resultados(url)
        if len(resultados) == 0:
            return await ctx.send("{} 0 resultados encontrados".format(user.mention))
        if len(resultados) == 1:
            return await self.por_na_fila(ctx, prioridade, resultados[0], voice_client)
        if len(resultados) > 1:
            for resultado in resultados:
                busca = await get_busca(resultado)
                await self.por_na_fila(ctx, 2, busca, voice_client)

    async def por_na_fila(self, ctx, prioridade, musica, voice_client):
        if prioridade != 2:
            self.fila[ctx.guild.id].insert(0, musica)
            if prioridade == 0 and voice_client.is_playing():
                return await self.skip(ctx)
        else:
            self.fila[ctx.guild.id].append(musica)

        if not voice_client.is_playing():
            await self.tocar_prox(ctx, voice_client)

    async def tocar_prox(self, ctx, voice_client):
        if len(self.fila[ctx.guild.id]) == 0:
            return await ctx.send(embed=discord.Embed(title="Fila Vazia", color=0xFF0000))

        musica = self.fila[ctx.guild.id].pop(0)
        if musica.local_file:
            musica.audio = os.getcwd() + "/music/" + musica.url
            ff_opts = {}
        else:
            await get_dados_musica(musica)
            ff_opts = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': "-vn"}

        if isinstance(musica.audio, Exception):
            mostra = musica.titulo or musica.url
            embed = discord.Embed(
                title="Nao encontrei {}".format(mostra), color=0xFF0000)
            embed.add_field(name="Erro:", value=str(
                musica.audio), inline=False)
            embed.add_field(name="Pedido por:",
                            value=ctx.author.mention, inline=False)
            return await ctx.send(embed=embed)

        embed = discord.Embed(title="Tocando agora:", color=0x008000)
        embed.add_field(name=musica.titulo, value=musica.url, inline=False)

        await ctx.send(embed=embed)
        player = discord.FFmpegPCMAudio(musica.audio, **ff_opts)

        voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.tocar_prox(ctx, voice_client), self.bot.loop))
        
        if self.repeat:
            self.fila[ctx.guild.id].append(musica)

    @commands.command(help="Skipa...", aliases=["s"])
    async def skip(self, ctx):
        user = ctx.author

        if canal_voz_invalido(user):
            return await ctx.send("{} Repete não te escuitei".format(user.mention))

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if voice_client.is_playing():
            voice_client.stop()
        else:
            return await ctx.send("{} Nao estou tocando".format(user.mention))

    @commands.command(help="Mostra a fila...", name="queue", aliases=["q", "fila"])
    async def mostra_queue(self, ctx):
        embed = discord.Embed(title="Fila:", color=0x0000ff)
        if len(self.fila[ctx.guild.id]) == 0:
            embed.add_field(name="Sem músicas na fila!",
                            value="--------------------", inline=False)
        else:
            for musica in self.fila[ctx.guild.id][:10]:
                embed.add_field(name=musica.titulo,
                                value=musica.url, inline=False)
            embed.add_field(name="Musicas na fila:",
                            value=str(len(self.fila[ctx.guild.id])))
        await ctx.send(embed=embed)

    @commands.command(help="Para de tocar né...")
    async def stop(self, ctx):
        user = ctx.author
        if canal_voz_invalido(user):
            return await ctx.send("{} Repete não te escuitei".format(user.mention))

        voice_client = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)

        if not voice_client:
            return await ctx.send("{} Nem to tocando louquinho da APAE".format(user.mention))

        await ctx.send("{} Parando e limpando a fila".format(user.mention))
        voice_client.stop()
        self.fila[ctx.guild.id].clear()

    @commands.command(help="Para de tocar né...")
    async def pause(self, ctx):
        user = ctx.author
        if canal_voz_invalido(user):
            return await ctx.send("{} Repete não te escuitei".format(user.mention))

        voice_client = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)

        if not voice_client:
            return await ctx.send("{} Nem to tocando louquinho da APAE".format(user.mention))

        if voice_client.is_playing():
            voice_client.pause()
            await ctx.send("{} Pausando".format(user.mention))
        else:
            voice_client.resume()
            await ctx.send("{} Mim resumiu...".format(user.mention))
