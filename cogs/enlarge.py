from discord.ext import commands
import discord


class Enlarge(commands.Cog):

    @commands.command('enlarge')
    async def enlarge(self, ctx: commands.Context, emote : discord.emoji.Emoji):
        await ctx.send(emote.url)
