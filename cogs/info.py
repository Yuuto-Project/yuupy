from discord.ext import commands
from utils.utils import color_hex_to_int,get_emote_url
import json
import random
import time


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pings = ['Pang', 'Peng', 'Pong', 'Pung']

    @commands.command()
    async def ping(self, ctx: commands.Context):
        curr = time.time()
        latency: float = round(ctx.bot.latency * 1000.0, 2)
        msg = await ctx.send('Pinging... 🏓')
        await msg.edit(content=f'🏓 {random.choice(self.pings)}! Latency is {round((time.time() - curr) * 1000.0, 2)}ms. API latency is {latency}ms.')

    @commands.command()
    async def route(self, ctx: commands.Context):
        return


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
