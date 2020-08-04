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


async def search_user(query: str) -> typing.List[discord.Member]:
    if len(query) == 0:
        return []
    member = None
