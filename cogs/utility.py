from discord.ext import commands
from utils.utils import search_user
from cogs.convert.convert import Convert
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

    @commands.command(description='Returns an enlarged emote.',
                      help='Get the permanent link of one or multiple emotes to see them in larger sizes.',
                      aliases=['emoji'])
    async def enlarge(self, ctx: commands.Context, *, args: typing.Optional[str]):
        if args is None or len(args) == 0:
            await ctx.send("Sorry, but you need to provide me an emote to use this command~!")
            return
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

        await ctx.send('{}, here you go~!\n{}'.format(ctx.author.mention, '\n'.join(emote_links)))

    @commands.command(description='Gets your own or someone\'s avatar.',
                      help='This command will get the permanent link of your own avatar, or someone else\'s avatar.',
                      aliases=['pfp'])
    async def avatar(self, ctx: commands.Context, user: typing.Optional[str] = ''):
        if user is None or len(user) == 0:
            await ctx.send('{}, Here ya go~!\n{}'.format(ctx.author.mention,
                                                         ctx.author.avatar_url_as(format='png', size=2048)))
            return
        member = search_user(ctx, user)
        if len(member) == 0:
            await ctx.send('{} Sorry, but I can\'t find that user'.format(ctx.author.mention))
            return
        await ctx.send('{}, Here ya go~!\n{}'.format(ctx.author.mention,
                                                     member[0].avatar_url_as(format='png', size=2048)))
    
    @commands.command(description='Convert units.',
                      help='This command will help you convert between units.',
                      aliases=['convert'],
                      usage='<target_unit> <value> - Ex: cvt lbs 31.3kg')
    async def cvt(self, ctx: commands.Context, target_unit: str = '', input: str = ''):
        # Conversion is handeled externally
        await Convert.cvt(self, ctx, target_unit, input)

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
