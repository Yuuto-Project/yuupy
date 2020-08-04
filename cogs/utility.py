from discord.ext import commands
from utils.utils import search_user
import discord
import re
import typing


EMOTE_REGEX = r'(<a?:\w+:\d+>)'
EMOTE_ID_REGEX = r'[^:]+(?=>)'
EMOTE_IS_ANIMATED_REGEX = r'(<a)'
EMOTE_BASE_LINK = 'https://cdn.discordapp.com/emojis/'


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.emote_regex = re.compile(EMOTE_REGEX)
        self.emote_id_regex = re.compile(EMOTE_ID_REGEX)
        self.emote_is_animated_regex = re.compile(EMOTE_IS_ANIMATED_REGEX)

    @commands.command()
    async def enlarge(self, ctx: commands.Context, *, args: str):
        result = self.emote_regex.search(args)
        if result is None:
            await ctx.send('Sorry, but you need to provide me an emote to use this command~!')
            return
        split = args.split(' ')
        emote_links = []
        for item in split:
            if self.emote_regex.search(item) is not None:
                for single in self.emote_regex.finditer(item):
                    suffix: str
                    if self.emote_is_animated_regex.search(single.group()) is not None:
                        suffix = '.gif'
                    else:
                        suffix = '.png'
                    emote_id = self.emote_id_regex.search(single.group())
                    emote_links.append(EMOTE_BASE_LINK + str(emote_id.group()) + suffix)
        await ctx.send('{}, here you go~!'.format(ctx.author.mention))
        for link in emote_links:
            await ctx.send(link)

    @commands.command()
    async def avatar(self, ctx: commands.Context, user: typing.Optional[str] = ''):
        if user is None or len(user) == 0:
            await ctx.send('{}, Here ya go~!'.format(ctx.author.mention))
            await ctx.send(ctx.author.avatar_url)
            return
        member = search_user(ctx, user)
        if len(member) == 0:
            await ctx.send('{} Sorry, but I can\'t find that user'.format(ctx.author.mention))
            return
        await ctx.send('{}, Here ya go~!'.format(ctx.author.mention))
        await ctx.send(member[0].avatar_url)


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
