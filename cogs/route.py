from discord.ext import commands
import json
import random
import discord
from utils.utils import color_hex_to_int


def get_emote_url(emote_id):
    return f'https://cdn.discordapp.com/emojis/{emote_id}.gif?v=1'


# TODO fix this hellish formatting
def get_route_embed(route, ending):
    return discord.Embed(title=f'Next: {route["name"]}, {ending}',
                         color=color_hex_to_int(route["color"]),
                         description=f"{route['description']} ending") \
        .set_thumbnail(url=get_emote_url(route['emoteId'])) \
        .add_field(name="Age", value=route["age"], inline=True) \
        .add_field(name="Birthday", value=route["birthday"], inline=True) \
        .add_field(name="Animal Motif", value=route["animal"], inline=True) \
        .set_footer(text=f"Play {route['name']}'s next. All bois are best bois.")


class Route(commands.Cog):
    def __init__(self):
        self.routes = json.load(open('assets/routes.json'))
        self.endings = ['perfect', 'good', 'bad', 'worst']

    @commands.command()
    async def route(self, ctx: commands.Context):
        route = random.choice(self.routes)
        ending = random.choice(self.endings)

        embed = get_route_embed(route, ending).set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
