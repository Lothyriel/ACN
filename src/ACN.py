import datetime
import os
import time

import discord
import discord.ext.commands as exc

from discord.ext import commands
from datetime import datetime

from dotenv import load_dotenv
from random import seed
from random import randint

from src.commands.Diversos import Diversos
from src.commands.envia.EnviaSojado import EnviaSojado
from src.commands.envia.EnviaHentai import EnviaHentai
from src.commands.music.MusicPlayer import MusicPlayer
from src.commands.music.SoundPad import SoundPad
from src.commands.music.Lyrics import Lyrics


class ACN(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents, command_prefix='!', case_insensitive=True)

        seed(time.time())
        self.random = randint
        self.iniciei = datetime.now()
        self.id_pirocudo = 244922703667003392

        self.player = MusicPlayer(self)
        self.add_cog(SoundPad(self.player))

        self.add_cog(self.player)
        self.add_cog(Diversos(self))
        self.add_cog(EnviaHentai(self))
        self.add_cog(EnviaSojado(self))
        self.add_cog(Lyrics(self))

        self.debug = False

        load_dotenv()
        self.run(os.getenv("TOKEN_BOT"))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if self.random(1, 101) == 100:
            await ctx.send("{} Comi teu cuzinho".format(ctx.author.mention))

        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print("{0} Estamos dentro".format(self.user))
        self.player.load()

        await self.change_presence(activity=discord.Game(name="Sexo na lan house"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, erro):
        if isinstance(erro, exc.UserNotFound):
            msg = "Usuário: {} não encontrado".format(erro.argument)

        elif isinstance(erro, exc.CommandOnCooldown):
            msg = "Comando em cooldown, espere {} segundos".format(round(erro.retry_after, 2))

        elif isinstance(erro, exc.MissingRequiredArgument):
            msg = "Ta faltando o argumento: {}".format(erro.param)

        elif isinstance(erro, exc.CommandNotFound):
            msg = "Digite direito...nem tem esse comando"

        elif isinstance(erro, discord.errors.NotFound):
            msg = "Não encontrei o {}".format(erro)

        else:
            msg = "Erro: {}".format(erro)

        await ctx.send("{} | {}".format(ctx.author.mention, msg))

    def eh_plebe(self, user):
        return user.id != self.id_pirocudo
