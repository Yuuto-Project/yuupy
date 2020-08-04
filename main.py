import os
import dotenv
from discord.ext import commands


EXTENSIONS = [
    'cogs.utility',
    'cogs.info',
    #'cogs.fun'
]

dotenv.load_dotenv()

bot = commands.Bot(command_prefix='y!')

if __name__ == '__main__':
    for extension in EXTENSIONS:
        bot.load_extension(extension)

bot.run(os.getenv('TOKEN'), bot=True, reconnect=True)
