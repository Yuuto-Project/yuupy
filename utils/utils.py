import json
from discord.ext import commands
import discord
from discord.embeds import Colour
import typing
import re
from PIL import ImageFont, ImageDraw, Image
from io import BytesIO
import textwrap
import random
from utils.TextWrap import TextWrapper

USER_MENTION_REGEX = re.compile(r'<@!?(\d{17,20})>')
USER_TAG = re.compile(r'(\S.{0,30}\S)\s*#(\d{4})')
DISCORD_ID = re.compile(r'\d{17,20}')
font = ImageFont.truetype('./assets/fonts/YuuPy_combined.ttf', 56)
flag = Image.open('./assets/images/dialog/flag_overlay.png')
textbox = Image.open('./assets/images/dialog/text_box.png')


def color_hex_to_0x(hex_str):
    return '0x' + hex_str.replace('#', '')


def color_hex_to_int(hex_str):
    return int(color_hex_to_0x(hex_str), 16)


def ignore_case(str1: str, str2: str) -> bool:
    if len(str1) == 0 or len(str2) == 0:
        return False
    return str1.upper() == str2.upper()


def search_user(ctx: commands.Context, query: str) -> typing.List[discord.Member]:
    if len(query) == 0:
        return []
    capture = USER_MENTION_REGEX.search(query)
    member: typing.Optional[discord.Member] = None
    members: typing.List[discord.Member] = ctx.guild.members
    if capture is not None:
        id = capture.group(1)
        member = ctx.guild.get_member(int(id))
    elif USER_TAG.search(query) is not None:
        capture = USER_TAG.search(query)
        user_name = capture.group(1)
        user_discriminator = capture.group(2)
        result = list(filter(lambda x: (x.nick is not None and x.nick == user_name) or
                                       (x.name == user_name and x.discriminator == user_discriminator), members))
        if len(result) > 0:
            member = result[0]
    elif DISCORD_ID.search(query) is not None:
        capture = DISCORD_ID.search(query)
        id = capture.group()
        member = ctx.guild.get_member(int(id))

    if member is not None:
        return [member]

    exact_match: typing.List[discord.Member] = []
    wrong_case: typing.List[discord.Member] = []
    starts_with: typing.List[discord.Member] = []
    contains: typing.List[discord.Member] = []
    lower_query = query.lower()

    for _member in members:
        lower_name = _member.name.lower()
        lower_nick: typing.Optional[str]
        if _member.nick is not None:
            lower_nick = _member.nick.lower()
        if (_member.nick is not None and _member.nick == query) or _member.name == query:
            exact_match.append(_member)
        elif (ignore_case(_member.name, query) or (
                _member.nick is not None and ignore_case(_member.nick, query))) and len(exact_match) <= 0:
            wrong_case.append(_member)
        elif (_member.name.lower().startswith(lower_query) or (
                _member.nick is not None and _member.nick.lower().startswith(lower_query))) and len(wrong_case) <= 0:
            starts_with.append(_member)
        elif (lower_query in _member.name.lower() or (
                _member.nick is not None and lower_query in _member.nick.lower())) and len(starts_with) <= 0:
            contains.append(_member)

    exact_match += wrong_case
    exact_match += starts_with
    exact_match += contains
    return exact_match


def get_emote_url(emote_id: str, format: str) -> str:
    return f'https://cdn.discordapp.com/emojis/{emote_id}.{format}?v=1'


def get_first_name(full_name: str) -> str:
    return full_name.split(' ')[0]


def render_dialog(text: str, character_name: str, background: str = 'camp') -> BytesIO:
    background = Image.open('./assets/images/dialog/backgrounds/' + background + '.png')
    character = Image.open('./assets/images/dialog/characters/' + character_name + '.png')
    # Remove "young_" prefix only here to find a ribbon, but still use the young sprite
    character_name = character_name.replace('young_', '')
    ribbon = Image.open('./assets/images/dialog/ribbons/' + character_name + '.png')

    # Start pasting onto the background image
    background.paste(character, (0, 0), character)
    background.paste(textbox, (0, 682), textbox)
    background.paste(ribbon, (0, 653), ribbon)
    # Paste flag in the top-right corner
    background.paste(flag, (background.size[0] - flag.size[0], 10), flag)

    draw = ImageDraw.Draw(background)
    # Wrap text
    text = "\n".join(textwrap.wrap(text, width=20))
    # Text box
    wrapper = TextWrapper(text, font, 940)
    wrapped_text = wrapper.wrapped_text()
    # Render text
    draw.multiline_text((80, 750), wrapped_text, font=font, fill="#FFF")

    # Generate the actual image
    result = BytesIO()
    background.save(result, "png")
    result.seek(0)

    return result


def status_embed(text: str, status=True) -> discord.Embed:
    embed = discord.Embed(description=text)

    if status:
        embed.title = "✅"
        # color is not modifiable
        embed.colour = discord.Color.green()
    else:
        embed.title = "Oops"
        embed.colour = discord.Color.red()

    return embed


def buddy_name_to_color(name: str) -> int:
    def filter_on_name(char_name: any):
        return get_first_name(char_name['name']).lower() == name

    with open('assets/chars.json') as c:
        chars = json.load(c)
        filtered = list(filter(filter_on_name, chars))

        if filtered:
            return color_hex_to_int(filtered[0]['color'])
        else:
            return Colour.blurple().value

def get_buddy_data(name: str = None):
    def filter_on_name(char_name: any):
        if char_name['name'].find(name.capitalize()) != -1:
            return True
        else: 
            return False

    with open('assets/chars.json') as c:
        chars = json.load(c)
        # If no name is given, return a random character
        if name is None:
            return random.choice(chars)
        else:
            filtered = list(filter(filter_on_name, chars))

        if filtered:
            return filtered[0]
        else:
            return None
