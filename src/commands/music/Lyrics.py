from discord.ext import commands

import requests

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Procura a letra na API do Vagalume")
    async def on_voice_state_update(self, ctx, *msg):
        meio = msg.index("-")

        musica = "+".join(msg[0:meio])
        artista = "+".join(msg[meio:])
        endpoint = "http://api.vagalume.com.br/search.php?art={}&mus={}".format(artista, musica)
        
        response = requests.get(endpoint).json()

        lyrics = response.mus

        if not lyrics:
            return await ctx.send("Não existe letras para {}".format(" ".join(msg)))

        await ctx.send(lyrics[0].text)