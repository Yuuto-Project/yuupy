from discord.ext import commands
from utils.utils import search_user
import json
import re
import typing


EMOTE_REGEX = r'(<a?:\w+:\d+>)'
EMOTE_ID_REGEX = r'[^:]+(?=>)'
EMOTE_IS_ANIMATED_REGEX = r'(<a)'
EMOTE_BASE_LINK = 'https://cdn.discordapp.com/emojis/'

def cvt_units(unit1: str, unit2: str, value: float):
    convert_dictionary = {
        # Lenght
        "km": {
            "km": 1,
            "m": 0.001,
            "cm": 1e-5,
            "in": 39370,
            "ft": 3280.84,
            "mi": 0.621371,
            "au": 6.68459e-9,
        },
        "m": {
            "km": 0.001,
            "m": 1,
            "cm": 100,
            "in": 39.37,
            "ft": 3.28084,
            "mi": 6.2137e-4,
            "au": 6.6846e-12
        },
        "cm": {
            "km": 1e-5,
            "m": 0.001,
            "cm": 1,
            "in": 0.3937,
            "ft": 0.0328,
            "mi": 6.2137e-6,
            "au": 6.68459e-14
        },
        "in": {
            "km": 2.54e-5,
            "m": 0.0254,
            "cm": 2.54,
            "in": 1,
            "ft": 0.0833,
            "mi": 1.5783e-5,
            "au": 1.6979e-13
        },
        "ft": {
            "km": 3.048e-4,
            "m": 0.3048,
            "cm": 30.48,
            "in": 12,
            "ft": 1,
            "mi": 1.8939e-3,
            "au": 2.0375e-12
        },
        "mi": {
            "km": 1.60934,
            "m": 1609.34,
            "cm": 160934,
            "in": 63360,
            "ft": 5280,
            "mi": 1,
            "au": 2.0375e-12
        },
        "au": {
            "km": 1.496e8,
            "m": 1.496e11,
            "cm": 1.496e13,
            "in": 5.89e12,
            "ft": 4.908e+11,
            "mi": 9.296e+7,
            "au": 1
        },
        # Weight
        "g": {
            "kg": 0.001,
            "g": 1,
            "lbs": 0.0022
        },
        "kg": {
            "kg": 1,
            "g": 1000,
            "lbs": 2.2
        },
        "lbs": {
            "kg": 0.453592,
            "g": 453.592,
            "lbs": 1
        }
    }

    output = 0.0
    error = False
    unit_source = unit1
    unit_target = unit2

    # Account for aliases
    if unit1 == "lb":
        unit1 = "lbs"
    if unit2 == "lb":
        unit2 = "lbs"

    # Use special calculations where it is not possible to use the Dictionary
    # Temperatures
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
    
    # If we don't need special calculations, use the Dictionary
    else:
        if unit1 in convert_dictionary and unit2 in convert_dictionary[unit1]:
            output = value * convert_dictionary[unit1][unit2]
        else:
            error = True

    if error:
        return 'This conversion is not possible!'
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
                    emote_links.append(EMOTE_BASE_LINK +
                                       str(emote_id.group()) + suffix)
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
            await ctx.send('{}{} is the equivalent of {}{}.'.format(answer[0], answer[2], answer[1], answer[3]))


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
