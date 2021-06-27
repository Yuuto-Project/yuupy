from cogs.minigame.minigame import Minigame
from discord.ext import commands
from io import BytesIO
from owoify.owoify import owoify
from typing import Optional, List, Tuple
from utils.utils import search_user, buddy_name_to_color as get_color
import asyncio
import discord
import json5
import requests
import os
from glob import glob
import random
from utils.CampBuddyMakov import CampBuddyMakov


def find_next_user(first: discord.Member, seconds: List[discord.Member]) -> Optional[discord.Member]:
    if len(seconds) == 0:
        return None
    elif len(seconds) == 1:
        return seconds[0]

    for member in seconds:
        if member.id == first.id:
            continue
        return member
    return None


def find_message(score: float, ship_messages: List[object]) -> str:
    single = list(filter(lambda x: score <= x['max_score'], ship_messages))
    return single[0]['message']


def calculate_score(first: discord.Member, second: discord.Member, ship_messages: List[object]) -> Tuple[float, str]:
    first_id: int = first.id
    second_id: int = second.id
    
    if first_id == second_id:
        return 100, 'You\'re a perfect match... for yourself!'
        
    if check_rig(first_id, second_id) or check_rig(second_id, first_id):
        score = 100
    else:
        score = ((first_id + second_id) // 7) % 100
    
    return score, find_message(score, ship_messages)

def check_rig(id1, id2):
    rigged = os.getenv(f'RIGGED_{id1}')
    if rigged == str(id2):
        return True
    else:
       return False

quote_enabled = bool(glob('./assets/quote/*.txt'))

if not quote_enabled:
    print('No quotes found, disabling command')


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open('assets/shipMessages.json5') as file_1:
            self.ship_messages = json5.loads(file_1.read())

        def parse_files(file: str):
            # strip off stuff that we don't need
            return file.replace('./assets/quote/', '').replace('.txt', '')

        if quote_enabled:
            fileNames = glob('./assets/quote/*.txt')
            self.charNames = list(map(parse_files, fileNames))

    @commands.command(description='Get a fake camp buddy quote', 
                      enabled=quote_enabled,
                      help='This command generates fake camp buddy quotes from the characters. It does this by '
                           'utilising a "makrov chain"', 
                      aliases=['quotation', 'saying'])
    async def quote(self, ctx: commands.Context, character: str = None):
        await ctx.trigger_typing()

        if character:
            char = character.lower()
            if char not in self.charNames:
                await ctx.send(f'I don\'t know who "{character}" is')
                return
        else:
            char = random.choice(self.charNames)

        with open(f'./assets/quote/{char}.txt') as lines:
            text = lines.read()

        # Build the model.
        text_model = CampBuddyMakov(text)
        generated = text_model.make_sentence()

        while not generated:
            generated = text_model.make_sentence()

        embed = discord.Embed(title=f'{char.capitalize()} once said', description=generated, color=get_color(char))

        await ctx.send(embed=embed)

    @commands.command(description='Calculate if you and your crush will work out.',
                      help='Yuuto mastered the art of shipping users and can now calculate if you and your crush will work out.',
                      usage='<user_1> <user_2>',
                      aliases=['love', 'ratecouple'])
    async def ship(self, ctx: commands.Context, username_1: str = '', username_2: str = ''):
        if username_1 == '' or username_2 == '':
            await ctx.send("You have to provide two usernames!")
            return

        search_result = search_user(ctx, username_1.lower())
        user_1: discord.Member
        if len(search_result) > 0:
            user_1 = search_result[0]
        else:
            await ctx.send(f'No user found for input `{username_1}`')
            return
        search_result = search_user(ctx, username_2.lower())
        user_2 = find_next_user(user_1, search_result)
        if user_2 is None:
            await ctx.send(f'No user found for input `{username_2}`')
            return

        img1 = user_1.avatar_url_as(static_format='png', size=256)
        img2 = user_2.avatar_url_as(static_format='png', size=256)

        score, message = calculate_score(user_1, user_2, self.ship_messages)
        response = requests.post('https://apis.duncte123.me/images/love',
                                 json={'image1': f'{img1}', 'image2': f'{img2}'},
                                 headers={
                                     'Content-Type': 'application/json',
                                     'User-Agent': 'Yuuto.py (https://github.com/Yuuto-Project/yuupy+)'
                                 })

        if not response:
            await ctx.send('Failed to ship these 2! Guess it\'s a doomed ship...')
            return

        message = message.replace('{name}', user_1.display_name).replace('{name2}', user_2.display_name)
        embed = discord.Embed(title='{} and {}'.format(user_1.display_name, user_2.display_name))
        embed = embed.add_field(name=f'Your love score is {int(score)}%', value=message, inline=False).set_image(
            url='attachment://result.png')
        await ctx.send(embed=embed, file=discord.File(fp=BytesIO(response.content), filename='result.png'))

    @commands.command(description='OwO-ify your text.',
                      help='Turn your sentences and texts to nonsensical babyspeaks (a.k.a. owoify). Currently, '
                           '3 levels of OwO are supported: **soft**, **medium**, **hard**',
                      usage='[level] <text>',
                      aliases=['owo'])
    async def owoify(self, ctx: commands.Context, level: Optional[str], *, text: Optional[str] = ''):
        result_text = ''
        if level is None:
            await ctx.send("You need to supply an input text!")
            return

        level = level.lower()
        if level == 'soft':
            result_text = owoify(text, 'owo')
        elif level == 'medium':
            result_text = owoify(text, 'uwu')
        elif level == 'hard':
            result_text = owoify(text, 'uvu')
        else:
            text = f'{level} {text}'
            result_text = owoify(text)
        author: discord.Member = ctx.author
        result_text = 'OwO-ified for {}~!\n\n{}'.format(author.mention, result_text.replace('`', '\\`').replace('*', '\\*'))
        await ctx.send(result_text)

    @commands.command(description='Play a fun quiz with your friends.',
                      help='Run `minigame` to begin a new game, and react within the countdown to join.',
                      uage='[rounds=7]',
                      aliases=['quiz', 'trivia'])
    async def minigame(self, ctx: commands.Context, rounds: Optional[int] = 7):
        if rounds < 2 or rounds > 10:
            await ctx.send('The number of rounds has to be greater than 1 and less than 11.')
            return
        game = await Minigame.create(ctx, rounds)
        if game is not None:
            asyncio.create_task(game.game(ctx))


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
