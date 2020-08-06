import os
import discord
import dotenv
from discord.ext import commands


EXTENSIONS = [
    'cogs.utility',
    'cogs.info',
    'cogs.fun'
]

dotenv.load_dotenv()
bot = commands.Bot(command_prefix='y!')


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

if __name__ == '__main__':
    for extension in EXTENSIONS:
        bot.load_extension(extension)

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)
