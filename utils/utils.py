from discord.ext import commands
import discord
import typing
import re

USER_MENTION_REGEX = re.compile(r'<@!?(\d{17,20})>')
USER_TAG = re.compile(r'(\S.{0,30}\S)\s*#(\d{4})')
DISCORD_ID = re.compile(r'\d{17,20}')


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
        elif (ignore_case(_member.name, query) or (_member.nick is not None and ignore_case(_member.nick, query))) and len(exact_match) <= 0:
            wrong_case.append(_member)
        elif (_member.name.lower().startswith(lower_query) or (_member.nick is not None and _member.nick.lower().startswith(lower_query))) and len(wrong_case) <= 0:
            starts_with.append(_member)
        elif (lower_query in _member.name.lower() or (_member.nick is not None and lower_query in _member.nick.lower())) and len(starts_with) <= 0:
            contains.append(_member)

    exact_match += wrong_case
    exact_match += starts_with
    exact_match += contains
    return exact_match


def get_emote_url(emote_id: str, format: str) -> str:
    return f'https://cdn.discordapp.com/emojis/{emote_id}.{format}?v=1'


def get_first_name(full_name: str) -> str:
    return full_name.split(' ')[0]
