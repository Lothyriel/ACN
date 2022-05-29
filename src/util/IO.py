import math

OUTPUT_BUFFER_LENGTH = 2000

async def send_long_text(ctx, text):
    n_slices = math.ceil(len(text) / OUTPUT_BUFFER_LENGTH)
        
    for i in range(n_slices):
        inicio = i * OUTPUT_BUFFER_LENGTH
        fim = (i + 1) * OUTPUT_BUFFER_LENGTH

        await ctx.send(text[inicio:fim])