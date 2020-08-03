import time
from discord.ext import commands


class Ping(commands.Cog):

    @commands.command('ping')
    async def ping(self, ctx : commands.Context):
        curr = time.time()
        msg = await ctx.send('Pinging 🏓')
        await msg.edit(content=f'Pong! Latency is {time.time() - curr}ms')
