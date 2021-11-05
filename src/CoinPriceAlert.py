import asyncio

import requests
from discord.ext import commands


async def get_valor_coin(id_coin):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, requests.get, "https://api.pancakeswap.info/api/v2/tokens/{}".format(id_coin))
    data = result.json().get("data", {"price": "0", "symbol": "F"})
    dol = data["price"]
    simbolo = data["symbol"]
    return "{}: {}".format(simbolo, round(float(dol), 2))


class CoinPriceNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Controlador = bot.Controlador

    @commands.command(help="Cria um alerta de preço !alert <contrato> <valor>")
    async def alert(self, ctx, contrato):
        loop = asyncio.get_event_loop()
        valor = await loop.run_in_executor(None, requests.get, "https://api.pancakeswap.info/api/v2/tokens/{}".format(contrato))

        if "error" in valor.json():
            return await ctx.author.send("Contrato inválido")

        coins = self.Controlador.coins
        if contrato not in coins:
            coins[contrato] = list()
        coins[contrato].append(str(ctx.author))
        coins.save_coins()
        