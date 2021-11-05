import asyncio
import os
import traceback
from datetime import datetime

import discord
import requests
from discord.ext import commands, tasks

from src import Controlador, Navegador
from src.CrowTracker.ScanResult import ScanResult, EResult
from src.Exceptions import TokenExpired, Manutencao, CancelaVarredura, ServerError


async def get_request_planta(id_planta):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_request, id_planta)


def get_request(id_planta):
    auth_token = os.getenv("BEARER_TOKEN")
    headers = {'Authorization': 'Bearer ' + auth_token}
    return requests.get("https://backend-farm.plantvsundead.com/farms/{}".format(id_planta), headers=headers).json()


class CrowTracker(commands.Cog):
    def __init__(self, bot):
        self.Controlador = bot.Controlador
        self.bot = bot

    @tasks.loop(minutes=1)
    async def roda_verificacao(self, token_valido=True):

        if not token_valido:
            await Navegador.get_novo_token()

        tasks_resultado = list()
        print("{} Iniciando varredura!".format(datetime.today()))
        await self.bot.change_presence(activity=discord.Game(name="Socando punheta"))
        for id_user, dados in dict(self.Controlador.contas).items():
            user = await self.bot.fetch_user(id_user)
            user_name = dados["user"]
            if not user:
                await self.bot.guilds[0].text_channels[0].send("Usuário {} não encontrado".format(user_name))
                continue

            for alias, plantas in dict(dados["aliases"]).items():
                for planta in plantas:
                    tasks_resultado.append(asyncio.create_task(self.resultado_verificacao(user, alias, planta)))
        try:
            await asyncio.gather(*tasks_resultado)
            print("Varredura finalizada!")
        except Exception as e:
            for t in tasks_resultado:
                t.cancel()

            Controlador.save_log("{} {} {} \nUser: {} Planta: {} {} \n{} \n{}".format(datetime.today().time(), "Varredura", "ACN", "Tracker", user, planta, e, traceback.format_exc()))

            if isinstance(e, TokenExpired):
                await self.roda_verificacao(False)

    @commands.command(help="Força o crow tracker a iniciar uma varredura e resetar o Bearer Token")
    async def roda(self, ctx):
        if self.bot.eh_plebe(ctx.author):
            return await ctx.send("Seu pau é infelizmente muito pequeno para utilizar este comando")
        await self.roda_verificacao(False)

    @commands.command(help="Mostra todas as plantas cadastradas na sua conta", name="list")
    async def get_list(self, ctx):
        user = ctx.author
        conta = self.Controlador.get_conta(user)
        embed = discord.Embed(title="Plantas de:", description=user.mention, color=0x00ff00)
        embed.add_field(name="Config Notificacoes:", value=conta["configs"])
        if not conta:
            embed.add_field(name="Sem aliases cadastrados!", inline=False)
        else:
            for alias, plantas in conta["aliases"].items():
                embed.add_field(name=alias, value="\n".join(plantas), inline=False)

        await ctx.send(embed=embed)

    @commands.command(help='!remove <alias>|"all" <id_planta>|opcional')
    async def remove(self, ctx, alias, id_planta=None):
        resultado_exclusao = self.Controlador.excluir_planta(str(ctx.author.id), alias, id_planta)
        await ctx.send("{0} {1}".format(ctx.author.mention, resultado_exclusao))

    @commands.command(help="!sub <apelido> <id_planta> <id_planta> <id_planta>...")
    async def sub(self, ctx, apelido, *ids_planta):
        user = ctx.author
        resultado_operacao = user.mention
        if len(ids_planta) > 0:
            for id_planta in ids_planta:
                resultado_operacao += self.Controlador.cadastrar_planta(user, apelido, id_planta)
        else:
            resultado_operacao += " Digite um apelido e pelo menos um id de planta"

        await ctx.send(resultado_operacao)

    @commands.command(help="Configurar notificacoes (0,1) <agua> <6 plantas>")
    async def config(self, ctx, regar, land_pobre):
        user = ctx.author
        conta = self.Controlador.get_conta(user)
        if not conta:
            return await ctx.send("{} Voce nem ta cadastrado teu...".format(user.mention))
        if land_pobre not in ("0", "1") or regar not in ("0", "1"):
            return await ctx.send("{} Opcao Invalida".format(user.mention))

        conta["configs"]["regar"] = regar
        conta["configs"]["landPobre"] = land_pobre
        self.Controlador.save_contas()
        return await ctx.send("{} Configuracoes de notificacao alteradas".format(user.mention))

    @commands.command(help="Comando secreto nao mexa",)
    async def altera(self, ctx):
        if self.bot.eh_plebe(ctx.author):
            return await ctx.send("Seu pau é infelizmente muito pequeno para utilizar este comando")

        for uid, dados in self.Controlador.contas.items():
            pass

        self.Controlador.save_contas()
        return await ctx.send("Alterado com sucesso")

    async def resultado_verificacao(self, user, alias, planta):
        request = await get_request_planta(planta)
        conta = self.Controlador.get_conta(user)

        def get_status():
            if "error" == request.get('message'):
                return ScanResult("Server error", ServerError())

            status = request["status"]

            if status == 1:
                return ScanResult("Token Expirou", TokenExpired())

            if status == 444:
                return ScanResult("Site em manutenção", Manutencao())

            if status == 27:
                msg = "Hora de colher planta do {} ".format(alias) + self.Controlador.excluir_planta(str(user.id), alias, planta)
                return ScanResult(msg, EResult.Mostra)

            data = request["data"]
            estado = data["stage"]
            precisa_agua = data["needWater"]
            tem_semente = data["hasSeed"]

            if tem_semente:
                return ScanResult("VOCE DROPOU UMA SEMENTE NO {} PORAAAAAAAAAAAAAAAAAAAAAA".format(alias), EResult.Mostra)

            if estado == "cancelled":
                msg = "Hora de colher planta do {} ".format(alias) + self.Controlador.excluir_planta(str(user.id), alias, planta)
                return ScanResult(msg, EResult.Mostra)

            if estado == "paused":
                return ScanResult("Corvo cacetando a planta do {}".format(alias), EResult.Mostra)

            if precisa_agua:
                return ScanResult("Tem que dar uma gozada na planta do {}".format(alias), EResult.Regar)

            #if len(conta["aliases"][alias]) != 6:
                #return ScanResult("{} esta pobre vc esqueceu de plantar".format(alias), EResult.LandPobre)

            if estado == "farming":
                return ScanResult("Tudo certo com a planta {}".format(planta), EResult.OK)

            msg = "ESTADO SECRETO JAMAIS IDENTIFICADO NA PLANTA {} CONTATE O JX MUNIDO DE PRINT DA PLANTA E DA MENSAGEM \n{}".format(planta, request)
            return ScanResult(msg, EResult.Mostra)

        status_planta = get_status()

        print("{} {} {}".format(user, alias, status_planta.Message))

        if status_planta.Result == EResult.OK:
            return

        if status_planta.Result == EResult.Mostra:
            return await user.send(status_planta.Message)

        if status_planta.Result == EResult.Regar and conta["configs"]["regar"] == "1":
            return await user.send(status_planta.Message)

        if status_planta.Result == EResult.LandPobre and conta["configs"]["landPobre"] == "1":
            return await user.send(status_planta.Message)

        if isinstance(status_planta.Result, CancelaVarredura):
            raise status_planta.Result

