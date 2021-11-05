from discord.ext import commands

class SoundPad(commands.Cog):
    def __init__(self, player):
        self.player = player

    @commands.command(help="eita mano")
    async def eita(self, ctx):
        await self.player.play(ctx, 0, 'eita.mp3')

    @commands.command(help="eu nao intindi o que ele falo")
    async def flamengo(self, ctx):
        await self.player.play(ctx, 0, 'flamengo.mp3')

    @commands.command(help="ce tenta ser o albi")
    async def oneda(self, ctx):
        await self.player.play(ctx, 0, 'oneda.mp3')

    @commands.command(help="FIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIUUU XXXXXXPAAAAAAAAAAAAAAAAAAAAAAAAAAAALAAAAAAAU")
    async def rojao(self, ctx):
        await self.player.play(ctx, 0, 'rojao.mp3')

    @commands.command(help="quero fazer sexo")
    async def yamete(self, ctx):
        await self.player.play(ctx, 0, 'yamete.mp3')

    @commands.command(help="é o buff familia")
    async def buff(self, ctx):
        await self.player.play(ctx, 0, 'buff.mp3')