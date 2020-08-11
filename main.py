import os
import discord
import dotenv
from cogs.minigame.minigame import Minigame
from discord.ext import commands
from typing import Union


EXTENSIONS = [
    'cogs.utility',
    'cogs.info',
    'cogs.fun'
]

dotenv.load_dotenv()
prefix = os.getenv('PREFIX') or 'y!'
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('Logged on as', bot.user)
    game = discord.Game('Volleyball')
    await bot.change_presence(activity=game, status=discord.Status.online)


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    else:
        await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: Union[discord.Member, discord.User]):
    standby_messages = list(filter(lambda x: x == reaction.message.id, Minigame.standby_messages))
    if len(standby_messages) == 0:
        return
    Minigame.register_player(reaction.message.channel.id, user)


if __name__ == '__main__':
    for extension in EXTENSIONS:
        bot.load_extension(extension)

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)
