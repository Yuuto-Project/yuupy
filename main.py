import os
import dotenv

from discord.ext import commands

from cogs.ping import Ping
from cogs.avatar import Avatar
from cogs.enlarge import Enlarge
from cogs.ship import Ship
from cogs.route import Route

dotenv.load_dotenv()

bot = commands.Bot('y!')

bot.add_cog(Ping())
bot.add_cog(Avatar())
bot.add_cog(Enlarge())
bot.add_cog(Ship())
bot.add_cog(Route())

bot.run(os.getenv('TOKEN'))
