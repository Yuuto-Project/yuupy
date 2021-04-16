import os
import discord
import dotenv
from discord.ext.commands import DisabledCommand

import help
from cogs.minigame.minigame import Minigame
from discord.ext import commands
from typing import Union


EXTENSIONS = [
    'cogs.utility',
    'cogs.info',
    'cogs.fun'
]

# The detailed and brief descriptions, plus aliases, of the command `help` itself.
HELP_TEXTS = {
    'description': 'To see a list of commands.',
    'help': 'This command will show all the commands available in Yuuto.',
    'aliases': ['manual']
}

intents = discord.Intents.default()
intents.members = True

# only try to load the env file if found, docker will use actual env vars
if os.path.exists('.env'):
    dotenv.load_dotenv()

prefix = os.getenv('PREFIX') or 'y!'
bot = commands.Bot(command_prefix=prefix, help_command=help.Help(HELP_TEXTS), intents=intents)


@bot.event
async def on_ready():
    print('Logged on as', bot.user)
    game = discord.Game('Volleyball')
    await bot.change_presence(activity=game, status=discord.Status.online)


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.guild is None:
        return

    botcmds = os.getenv(f'BOTCMDS_{message.guild.id}')

    if botcmds is not None and int(botcmds) != message.channel.id:
        return

    try:
        await bot.process_commands(message)
    except DisabledCommand:
        pass



@bot.event
async def on_reaction_add(reaction: discord.Reaction, user: Union[discord.Member, discord.User]):
    standby_messages = list(filter(lambda x: x == reaction.message.id, Minigame.standby_messages))
    if len(standby_messages) == 0:
        return
    if user.bot:
        return
    Minigame.register_player(reaction.message.channel.id, user)


@bot.event
async def on_reaction_remove(reaction: discord.Reaction, user: Union[discord.Member, discord.User]):
    standby_messages = list(filter(lambda x: x == reaction.message.id, Minigame.standby_messages))
    if len(standby_messages) == 0:
        return
    if user.bot:
        return
    Minigame.deregister_player(reaction.message.channel.id, user)


if __name__ == '__main__':
    for extension in EXTENSIONS:
        bot.load_extension(extension)

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)
