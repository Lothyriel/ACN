from discord.ext import commands

import requests


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Procura a letra na API do Vagalume")
    async def lyrics(self, ctx, *msg):
        data = ' '.join(msg)

        meio = data.index("-")

        musica = data[meio+1:].replace(' ', '+')

        artista = data[0:meio].replace(' ', '+')

        endpoint = f"http://api.vagalume.com.br/search.php?art={artista}&mus={musica}"

        response = requests.get(endpoint).json()    

        lyrics = response['mus'][0]['text']

        if not lyrics:
            return await ctx.send("Não existe letras para {}".format(" ".join(msg)))

        lyrics = list(lyrics)

        while len(lyrics):
            slice = ''.join(lyrics[0:500])
            del lyrics[0:500]
            await ctx.send(slice)
