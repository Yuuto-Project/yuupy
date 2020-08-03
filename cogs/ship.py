from discord.ext import commands
import discord


class Ship(commands.Cog):
    @commands.command('ship')
    async def ship(self, ctx: commands.Context, user1: discord.User, user2: discord.User):
        await ctx.send(f'Your love with {user1.name} and {user2.name} is x')
