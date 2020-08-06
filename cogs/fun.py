from discord.ext import commands
from owoify.owoify import owoify
from typing import Optional
import discord


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(description='Calculate if you and your crush will work out.',
                      help='Yuuto mastered the art of shipping users and can now calculate if you and your crush will work out.',
                      aliases=['love', 'ratecouple'])
    async def ship(self, ctx: commands.Context):
        await ctx.send('This command is not yet implemented.')

    @commands.command(description='Owoify your text.',
                      help='Turn your sentences and texts to nonsensical babyspeaks (a.k.a. owoify). Using `y!owoify <text>` will make use of the default owoify level (owo), which is the most vanilla one. Using `y!owoify [level] <text>` will explicitly set the owoify level. Currently, 3 levels are supported (from the lowest to the highest): **soft**, **medium**, **hard**')
    async def owoify(self, ctx: commands.Context, level: Optional[str], *, text: str):
        result_text = ''
        if len(level) > 0 and level != '':
            level = level.lower()
            if level == 'soft':
                result_text = owoify(text, 'owo').replace('`', '\\`').replace('*', '\\*')
            elif level == 'medium':
                result_text = owoify(text, 'uwu').replace('`', '\\`').replace('*', '\\*')
            elif level == 'hard':
                result_text = owoify(text, 'uvu').replace('`', '\\`').replace('*', '\\*')
            else:
                text = f'{level} {text}'
                result_text = owoify(text).replace('`', '\\`').replace('*', '\\*')
        author: discord.Member = ctx.author
        result_text = 'OwO-ified for {}~!\n\n{}'.format(author.mention, result_text)
        await ctx.send(result_text)


def setup(bot: commands.Bot):
    bot.add_cog(Fun(bot))
