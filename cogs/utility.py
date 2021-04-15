from discord.ext import commands
from utils.utils import search_user
from utils.convert_dictionary import get_convert_dictionary
import re
import typing

EMOTE_REGEX = r'(<a?:\w+:\d+>)'
EMOTE_ID_REGEX = r'[^:]+(?=>)'
EMOTE_IS_ANIMATED_REGEX = r'(<a)'
EMOTE_BASE_LINK = 'https://cdn.discordapp.com/emojis/'


# Account for Aliases during conversion
def parse_alias(unit):
    if unit == "lb":
        return "lbs"
    else:
        return unit


# Return metric relationship to its base unit (g, m, ...), or 1 if
# not metric, or input is already a metric base unit
# Do not change 1 to False, as the return value gets used for later arithmetic operations
def check_metric(input):
    metric_regx = "([umk][g]|[mcdh][l]|[umcdk][m])"
    metric_match = re.match(metric_regx, input)
    if metric_match is None:
        return 1

    multiplier = {
        "u": 1e-6,
        "m": 1e-3,
        "c": 0.01,
        "d": 0.1,
        "k": 1000
    }
    return multiplier[input[-2]]


def cvt_units(unit1: str, unit2: str, unit2_metr: str, value: float):
    # The dictionary is stored in a separate script
    convert_dictionary = get_convert_dictionary()

    output = 0.0
    error = False
    unit_source = unit1
    unit_target = unit2

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
            output = value * 9 / 5 + 32
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
                output = (value - 32) * 5 / 9 + 273.15
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
                output = (value - 273.15) * 9 / 5 + 32
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
        return [value, output, unit_source, unit2_metr + unit_target]


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
                      help='This command will help you convert between units. Ex: `cvt m 1ft`.',
                      aliases=['convert'])
    async def cvt(self, ctx: commands.Context, target_unit: str = '', input: str = ''):
        # Convert target unit to lower case. 
        # Might need removing in the future for compatibility reasons.
        target_unit = target_unit.lower()
        target_unit = parse_alias(target_unit)

        # Ensure parameters exist
        if not target_unit:
            await ctx.send("Please provide a target unit.")
            return
        if not input:
            await ctx.send("Please provide a source value.")
            return

        # Ensure target unit is known
        # A more complex implementation will be needed if conflicting types
        # such as seconds are added (s & lbs)
        convert_dictionary = get_convert_dictionary()
        if target_unit not in convert_dictionary and target_unit[-1] not in convert_dictionary:
            await ctx.send("Unknown target unit.")
            return

        # Regular expressions for parsing the unit and value from the input value
        unit_regx = "\\D{1,3}"
        value_regx = "-?[\\d.]+"

        # Check if the source value is numerical and suffixed by a unit
        input_match = re.match("(%s)(%s)" % (value_regx, unit_regx), input)

        if input_match is None:
            await ctx.send("I don't understand what you mean by {}.".format(input))
            return
        # In theory, this should never trigger
        if input_match.string != input:
            await ctx.send(
                "I don't understand what you mean by {}.".format(input) +
                " (Type assertion failed, please contact the developers ASAP.)")
            return

        # Get the source unit and value
        # Note: .lower() might need removing in the future for compatibility reasons.
        source_value = int(re.findall(value_regx, input)[0])
        source_unit = re.findall(unit_regx, input)[0].lower()
        source_unit = parse_alias(source_unit)

        # Ensure source unit is known
        # Source and target units could be checked together for a more 'elegant' solution
        # A more complex implementation will be needed if conflicting types
        # such as seconds are added (s & lbs)
        if source_unit not in convert_dictionary and source_unit[-1] not in convert_dictionary:
            await ctx.send("Unknown source unit.")
            return

        # Check and apply logic if we are using the metric system as an input
        metric_multiplier_inp = check_metric(source_unit)
        if metric_multiplier_inp != 1:
            source_unit = input[-1]
            source_value *= metric_multiplier_inp

        # Get appropriate target unit, if of the metric system
        target_unit_metric = ""
        metric_multiplier_res = check_metric(target_unit)
        if metric_multiplier_res != 1:
            target_unit_metric = target_unit[-2]
            target_unit = target_unit[-1]

        answer = cvt_units(source_unit, target_unit, target_unit_metric, source_value)
        if isinstance(answer, str):
            await ctx.send(answer)
        elif isinstance(answer, list):
            if metric_multiplier_inp != 1:
                source_value /= metric_multiplier_inp
                answer[2] = input[-2] + input[-1]
            answer[1] /= metric_multiplier_res
            answer[1] = round(answer[1], 2)
            await ctx.send('{}{} is the equivalent of {}{}.'.format(source_value, answer[2], answer[1], answer[3]))


def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
