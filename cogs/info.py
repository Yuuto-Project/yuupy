from discord.ext import commands
from utils.utils import color_hex_to_int, get_emote_url, get_first_name, render_dialog, status_embed
import discord
import json
import time
import glob
import random
import os
import asyncio


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pings = ['Pang', 'Peng', 'Pong', 'Pung']
        self.endings = ['Perfect', 'Good', 'Bad', 'Worst']

        self.dialog.backgrounds = [os.path.splitext(os.path.basename(x))[0]
                                   for x in glob.glob('./assets/images/dialog/backgrounds/*.png')]
        self.dialog.characters = [os.path.splitext(os.path.basename(x))[0]
                                  for x in glob.glob('./assets/images/dialog/characters/*.png')]

        self.dialog.backgrounds.sort()
        self.dialog.characters.sort()

        self.dialog.backgrounds_string = f"`{'`, `'.join(self.dialog.backgrounds)}`"
        self.dialog.characters_string = f"`{'`, `'.join(self.dialog.characters)}`"

        with open('assets/routes.json', 'r', encoding='utf-8') as raw_routes:
            self.routes = json.load(raw_routes)

    @commands.command(description='Get current latency and API ping.',
                      help='Send a ping to the bot and get latency information.', aliases=['pong'])
    async def ping(self, ctx: commands.Context):
        curr = time.time()
        latency: float = round(ctx.bot.latency * 1000.0, 2)
        msg = await ctx.send('Pinging... 🏓')
        await msg.edit(
            content=f'🏓 {random.choice(self.pings)}! Latency is {round((time.time() - curr) * 1000.0, 2)}ms. API latency is {latency}ms.')

    @commands.command(description='Tells you what route to play next.',
                      help='This command will let Yuuto decide which route you should play next.', aliases=['r'])
    async def route(self, ctx: commands.Context):
        author: discord.Member = ctx.author
        route = random.choice(self.routes)
        ending = random.choice(self.endings)
        embed = discord.Embed(title=f'Next: {route["name"]}, {ending} Ending',
                              color=color_hex_to_int(route["color"]),
                              description=f"{route['description']}") \
            .set_author(name=author.display_name, icon_url=author.avatar_url) \
            .set_thumbnail(url=get_emote_url(route['emoteId'], 'gif')) \
            .add_field(name="Age", value=route["age"], inline=True) \
            .add_field(name="Birthday", value=route["birthday"], inline=True) \
            .add_field(name="Animal Motif", value=route["animal"], inline=True) \
            .set_footer(text=f"Play {get_first_name(route['name'])}'s route next. All bois are best bois.")
        await ctx.send(embed=embed)

    @commands.command(description='Shows the Buddy Laws by Yuri.', help='Every camper should know this!')
    async def law(self, ctx: commands.Context):
        title = "The Buddy Law"
        desc = "1) A buddy should be kind, helpful, and trustworthy to each other!\n" \
               "2) A buddy must be always ready for anything!\n" \
               "3) A buddy must always show a bright smile on his face!\n" \
               "||4) We leave no buddy behind!||"
        embed = discord.Embed(title=title, description=desc, color=discord.Colour(0xFDBBE4))

        await ctx.send(embed=embed)

    @commands.command(description='Generates an image of a character in Camp Buddy saying anything you want.', help='This command will generate an image of a character in Camp Buddy saying anything you want.', aliases=['dialogue'])
    async def dialog(self, ctx: commands.Context, *, args: str = ''):
        if args == '':
            await ctx.send('This command requires at least two arguments: `dialog [background] <character> <text>` (['
                           '] is optional)')
            return

        splitted = args.split(' ')
        character = splitted.pop(0).lower()

        await ctx.trigger_typing()
        bg_def = ""

        if character in self.dialog.characters:
            bg_def = "\nNo background supplied, defaulting to Camp. Use `dialog [background] <character> <message>` to set a background!"
            background = "camp"
        else:
            background = character
            character = splitted.pop(0).lower()

        if background not in self.dialog.backgrounds:
            await ctx.send(f"Sorry, but I couldn't find {background} as a location\nAvailable backgrounds are: {self.dialog.backgrounds_string}")
            return

        if character not in self.dialog.characters:
            await ctx.send(f"Sorry, but I couldn't find {character} as a location\nAvailable characters are: {self.dialog.characters_string}")
            return

        text = " ".join(splitted[0:])

        if len(text) > 140:
            await ctx.send('Sorry, but the message limit is 140 characters :hiroJey:')
            return

        output = render_dialog(text, character, background)

        file = discord.File(filename="res.png", fp=output)

        await ctx.send(f"{ctx.author.mention}, Here you go! {bg_def}", file=file)

    @commands.command(description="Shows information about Yuuto", help="Shows information about yuuto",
                      aliases=["info", "bot", "credits"])
    async def about(self, ctx: commands.Context):
        inv = "https://discord.com/oauth2/authorize?client_id=684395509045264429&permissions=378944&scope=bot"
        desc = "Yuuto was made and developed by the community, for the community. \n" \
              "Join the dev team and start developing on the project's [GitHub page](https://github.com/Yuuto-Project/yuupy/). \n" \
              f"You can also join our [Discord server](https://discord.gg/fPFbV8G). \n" \
              f"[Click here]({inv}) to invite the bot to your own server! \n\n" \
              "Yuuto was developed by: \n" \
              "**Arch#0226**, **dunste123#0129**, **Tetsuki Syu#1250**, **zsotroav#8941**"
        embed = discord.Embed(title="About Yuuto!", description=desc, color=discord.Colour(0xFDBBE4)) \
            .set_author(
            name="Yuuto from Camp Buddy",
            url="https://blitsgames.com",
            icon_url="https://cdn.discordapp.com/emojis/593518771554091011.png")

        await ctx.send(embed=embed)

    @commands.command(description="Gives you the invite link for yuuto", help="Invite yuuto to your server!")
    async def invite(self, ctx: commands.Context):
        await ctx.send("You can invite me using this link: "
                       "<https://discord.com/oauth2/authorize?client_id=684395509045264429&permissions=378944&scope"
                       "=bot>")

    @commands.command(description='Help yuuto by giving us a suggestion or a bug report!', help="This command will let you help yuuto by giving it a suggestion or a bug report!", aliases=['suggestion'])
    async def suggest(self, ctx: commands.Context, *, args: str = None):
        suggestchannel: discord.TextChannel = await ctx.bot.fetch_channel(os.getenv('SUGGESTIONS_CHANNEL'))

        author: discord.User = ctx.author

        if args is None:
            await ctx.send(embed=status_embed("Message cannot be empty!", False))
            return

        embed = discord.Embed(title="Suggestion", description=args, color=discord.Color.blurple())\
            .set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)\
            .set_footer(text="React ✅ to confirm the submission of message, react ❌ to cancel")

        sentembed: discord.Message = await ctx.send(embed=embed)

        await sentembed.add_reaction('✅')
        await sentembed.add_reaction('❌')

        def check(reaction: discord.Reaction, user):
            return user == ctx.author and reaction.message.id == sentembed.id and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

        async def cancel():
            await ctx.message.delete()
            await sentembed.delete()
            await ctx.send('❌ Cancelled')

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            # Timeout
            await cancel()
        else:
            if reaction.emoji == '❌':
                await cancel()
            else:
                await suggestchannel.send(f"From {author.display_name}\n{args}")
                await ctx.send(embed=status_embed('Submitted! Thank you for helping this community project!'))


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
