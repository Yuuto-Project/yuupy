from discord.ext import commands
from utils.utils import search_user
import json
import re
import typing


EMOTE_REGEX = r'(<a?:\w+:\d+>)'
EMOTE_ID_REGEX = r'[^:]+(?=>)'
EMOTE_IS_ANIMATED_REGEX = r'(<a)'
EMOTE_BASE_LINK = 'https://cdn.discordapp.com/emojis/'

with open('assets/convert.json', 'r', encoding='utf-8') as file:
    raw_convert_table = file.read()
    convert_table: typing.Dict[object, object] = json.loads(raw_convert_table)


def cvt_units(unit1: str, unit2: str, value: float):
    # Convert temperature units
    output = 0.0
    error = False
    unit_source = ''
    unit_target = ''
    if unit1 == 'c':
        unit_source = '\u2103'
        if unit1 == unit2:
            output = value
            unit_target = unit_source
        elif unit2 == 'k':
            output = value + 273.15
            unit_target = 'K'
        elif unit2 == 'f':
            output = value * 9/5 + 32
            unit_target = '\u2109'
        else:
            error = True
    elif unit1 == 'f':
        unit_source = '\u2109'
        if unit1 == unit2:
            output = value
            unit_target = unit_source
        else:
            output = (value - 32) * 5 / 9
            if unit2 == 'c':
                unit_target = '\u2103'
            elif unit2 == 'k':
                output = (value - 32) * 5/9 + 273.15
                unit_target = 'K'
            else:
                error = True
    elif unit1 == 'k':
        unit_source = 'K'
        if unit1 == unit2:
            output = value
            unit_source = unit_target
        else:
            output = value - 273.15
            if unit2 == 'c':
                unit_target = '\u2103'
            elif unit2 == 'f':
                output = (value - 273.15) * 9/5 + 32
                unit_target = '\u2109'
            else:
                error = True
    elif unit1 == 'g':
        unit_source = unit1
        if unit1 == unit2:
            output = value
            unit_target = unit_source
        elif unit2 == 'kg':
            output = value * 0.001
            unit_target = 'kg'
        elif unit2 == 'lbs' or unit2 == 'lb':
            output = value * 0.0022
            unit_target = 'lbs'
        else:
            error = True
    elif unit1 == 'kg':
        unit_source = unit1
        if unit1 == unit2:
            output = value
            unit_target = unit_source
        elif unit2 == 'g':
            output = value * 1000
            unit_target = 'g'
        elif unit2 == 'lbs' or unit2 == 'lb':
            output = value * 2.2
            unit_target = 'lbs'
        else:
            error = True
    elif unit1 == 'lbs' or unit1 == 'lb':
        unit_source = 'lbs'
        if unit1 == unit2:
            output = value
            unit_target = unit_source
        elif unit2 == 'kg':
            output = value / 2.2
            unit_target = 'kg'
        elif unit2 == 'g':
            output = (value / 2.2) * 1000
            unit_target = 'g'
        else:
            error = True
    else:
        cvt_factor = convert_table['length'].get(unit2)
        if cvt_factor == None:
            error = True
        else:
            cvt_factor = cvt_factor.get(unit1)
            if cvt_factor == None:
                error = True
            else:
                output = value * cvt_factor
                unit_source = unit1
                unit_target = unit2
    if error:
        return 'This is not possible!'
    else:
        output = round(output, 2)
        return [value, output, unit_source, unit_target]


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
            await ctx.send("Sorry, but you need to provide me an emote or avatar to use this command~!")
            return
        member = search_user(ctx, args)
        if len(member) > 0:
            await ctx.send('{}, Here ya go~!'.format(ctx.author.mention))
            await ctx.send(member[0].avatar_url)
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
        await ctx.send('{}, here you go~!'.format(ctx.author.mention))
        for link in emote_links:
            await ctx.send(link)

    @commands.command(description='Gets your own or someone\'s avatar.',
                      help='This command will get the permanent link of your own avatar, or someone else\'s avatar.',
                      aliases=['pfp'])
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

    @commands.command(description='Convert units.',
                      help='This command will help you convert between units.',
                      aliases=['convert'])
    async def cvt(self, ctx: commands.Context, unit1: str, unit2: str, value: typing.Optional[float] = 0.0):
        answer = cvt_units(unit1, unit2, value)
        if isinstance(answer, str):
            await ctx.send(answer)
        elif isinstance(answer, list):
            await ctx.send('{}{} is equal to {}{}.'.format(answer[0], answer[2], answer[1], answer[3]))


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
