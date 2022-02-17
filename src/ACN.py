import datetime
import os

import discord
from discord.ext import commands, tasks
from datetime import datetime

import discord.ext.commands as exc
from dotenv import load_dotenv
from random import seed
from random import randint
import time

from src import CoinPriceAlert
from src.Diversos import Diversos
from src.EnviaHentai import EnviaHentai
from src.music.MusicPlayer import MusicPlayer
from src.Navegador import Navegador
from src.music.SoundPad import SoundPad


class ACN(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(intents=intents, command_prefix='!', case_insensitive=True)

        seed(time.time())
        self.random = randint
        self.iniciei = datetime.now()
        self.id_pirocudo = 244922703667003392
        # self.Controlador = C.Controlador()
        # self.CrowTracker = CrowTracker(self)
        self.Selenium = Navegador(self)

        player = MusicPlayer(self)
        self.add_cog(player)
        self.add_cog(SoundPad(player))

        # self.add_cog(CoinPriceNotifier(self))
        self.add_cog(Diversos(self))
        self.add_cog(EnviaHentai(self))

        self.add_cog(self.Selenium)
        # self.add_cog(self.CrowTracker)
        load_dotenv()
        self.run(os.getenv("TOKEN_BOT"))

    @commands.Cog.listener()
    async def on_command(self, ctx):
        contexto = ctx.guild.name if ctx.guild else "PV"
        user = str(ctx.author)
        command = ctx.command.name
        prefix = "!{}".format(command)
        args = ctx.message.content.replace(prefix, "")
        data = datetime.today().time()
        if self.random(1, 101) == 100:
            await ctx.send("{} Comi teu cuzinho".format(ctx.author.mention))
        # C.save_log("{} {} {} {} {}".format(data, contexto, user, command, args.strip()))
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print("{0} Estamos dentro".format(self.user))
        status = self.set_status

        if not status.is_running():
            status.start()

    @tasks.loop(seconds=10)
    async def set_status(self):
        await self.change_presence(activity=discord.Game(name=await CoinPriceAlert.get_valor_coin("0xfa57ff4670f9016069e799a51a3186d03991e431")))
        print("Atualizando status")

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
