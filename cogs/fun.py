from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ship(self, ctx: commands.Context):
        await ctx.send('This command is not yet implemented.')


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))