from discord.ext import commands

import requests


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Procura a letra na API do Vagalume  <artista-música>")
    async def lyrics(self, ctx, *msg):
        data = ' '.join(msg)
        meio = data.index("-")
        musica = data[meio + 1 : ].replace(' ', '+')
        artista = data[0 : meio].replace(' ', '+')

        endpoint = f"http://api.vagalume.com.br/search.php?art={artista}&mus={musica}"

        response = requests.get(endpoint).json()

        if response['type'] == 'notfound':
            return await ctx.send(f"Não existe letras para {data}")

        lyrics = response['mus'][0]['text']

        inicio = 0
        fim = 2000
        while len(lyrics[inicio:fim]):
            await ctx.send(lyrics[inicio:fim])
            inicio = inicio + 2000
            fim = fim + 2000
