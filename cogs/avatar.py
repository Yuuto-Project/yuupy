from discord.ext import commands
import discord


class Avatar(commands.Cog):

    @commands.command('avatar')
    async def avatar(self, ctx: commands.Context, mention: discord.User):
        await ctx.send(mention.avatar_url)

    @commands.command('avatar')
    async def avatar(self, ctx: commands.Context):
        await ctx.send(ctx.author.avatar_url)