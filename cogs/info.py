from discord.ext import commands
from utils.utils import color_hex_to_int, get_emote_url, get_first_name, get_buddy_data, render_dialog, status_embed
import discord
import json
import time
import glob
import random
import os
import asyncio

# suggest_enabled = bool(os.getenv('SUGGESTIONS_CHANNEL'))
# if not suggest_enabled:
#     print('Suggestions channel not set, disabling command.')

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
                      help='Send a ping to the bot and get latency information.', 
                      aliases=['pong'])
    async def ping(self, ctx: commands.Context):
        curr = time.time()
        latency: float = round(ctx.bot.latency * 1000.0, 2)
        msg = await ctx.send('Pinging... 🏓')
        await msg.edit(
            content=f'🏓 {random.choice(self.pings)}! Latency is {round((time.time() - curr) * 1000.0, 2)}ms. API latency is {latency}ms.')

    @commands.command(description='Tells you what route to play next.',
                      help='This command will let Yuuto decide which route you should play next.', 
                      aliases=['r'])
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

    @commands.command(description='Show information about a specific character.',
                      help='This command will show information about a specific character..', 
                      usage='<character>',
                      aliases=['character'])
    async def char(self, ctx: commands.Context, char: str = ''):
        char_data = get_buddy_data(char) # utils.utils.get_buddy_data()
        if char_data is None:
            await ctx.send(f"I don't know who {char} is.")
            return

        embed = discord.Embed(description=char_data['description'],
                              color=color_hex_to_int(char_data['color']))\
                            .set_author(name=char_data['name'], icon_url=f"https://cdn.discordapp.com/emojis/{char_data['cuteEmoteId']}.png")\
                            .add_field(name='Age', value=char_data['age'])\
                            .add_field(name='Birthday', value=char_data['birthday'])\
                            .add_field(name='Animal motif', value=char_data['animal'])\
                            .add_field(name='Height', value=char_data['height'])\
                            .add_field(name='Weight', value=char_data['weight'])\
                            .add_field(name='Blood Type', value=char_data['blood_type'])
        await ctx.send(embed=embed)

    @commands.command(description='Shows the Buddy Laws by Yuri.', 
                      help='Every camper should know this!')
    async def law(self, ctx: commands.Context):
        title = "The Buddy Law"
        desc = "1) A buddy should be kind, helpful, and trustworthy to each other!\n" \
               "2) A buddy must be always ready for anything!\n" \
               "3) A buddy must always show a bright smile on his face!\n" \
               "||4) We leave no buddy behind!||"
        embed = discord.Embed(title=title, description=desc, color=discord.Colour(0xFDBBE4))

        await ctx.send(embed=embed)

    @commands.command(description='Generates an image of a character in Camp Buddy saying anything you want.', 
                      help='This command will generate an image of a character in Camp Buddy saying anything you want.', 
                      usage='[background=camp] <character> <text>',
                      aliases=['dialogue'])
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

    @commands.command(description="Shows information about Yuuto", 
                      help="Shows information about Yuuto",
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

    @commands.command(description="Gives you the invite link for Yuuto", 
                      help="Invite Yuuto to your server!")
    async def invite(self, ctx: commands.Context):
        await ctx.send("You can invite Yuuto using this link: "
                       "<https://discord.com/oauth2/authorize?client_id=684395509045264429&permissions=378944&scope=bot>")

    # This command got disabled due to the concern of trolls abusing it
    # @commands.command(description='Help Yuuto by giving us a suggestion or a bug report!', 
    #                   enabled=suggest_enabled, 
    #                   help='This command will let you help Yuuto by giving it a suggestion or a bug report!', 
    #                   usage='<message>',
    #                   aliases=['suggestion'])
    async def suggest_old(self, ctx: commands.Context, *, args: str = None):
        # Check if we have access to the suggestion channel
        try:
            suggestchannel: discord.TextChannel = await ctx.bot.fetch_channel(os.getenv('SUGGESTIONS_CHANNEL'))
        except:
            await ctx.send("An error occured: I can't find the suggestions channel")
            print("Couldn't find suggestions channel!")
            return

        author: discord.User = ctx.author

        if args is None:
            await ctx.send(embed=status_embed("Message cannot be empty!", False))
            return
        
        # Show a confirmation message befor submitting
        # await ctx.message.delete()
        embed = discord.Embed(title="Suggestion", 
                              description=args, 
                              color=discord.Color.blurple())\
            .set_author(name=author.display_name, icon_url=author.avatar_url)\
            .set_footer(text="React with ✅ to confirm or with ❌ to cancel the submission of the message. \n"\
                             "Your username, user id, and server id will be submitted with the suggestion.")

        sentembed: discord.Message = await ctx.send(embed=embed)

        await sentembed.add_reaction('✅')
        await sentembed.add_reaction('❌')

        def check(reaction: discord.Reaction, user):
            return user == author and reaction.message.id == sentembed.id and (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌')

        async def cancel():
            embed_cancel = discord.Embed(title="Cancelled ❌", 
                                      description='Cancelled the suggestion', 
                                      color=discord.Color.red())\
                    .set_author(name=author.display_name, icon_url=author.avatar_url)
            await sentembed.delete()
            await ctx.send(embed=embed_cancel)
            return

        # Wait for added reactions
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            # Timeout after 10 secunds
            await cancel()
        else:
            # If didn't react with confirm, cancel
            if reaction.emoji != '✅':
                await cancel()
                return

            # Send the suggestion to the dev server
            embed_suggest = discord.Embed(description=args,
                                          color=discord.Color.green())\
                    .set_author(name=f"{author.display_name} ({author.id})", 
                                icon_url=author.avatar_url,
                                url=f"https://discord.com/users/{author.id}")\
                    .set_footer(text=f"From {ctx.guild.name} ({ctx.guild.id})")
            await suggestchannel.send(embed=embed_suggest)
            
            # Send a confirmation message to the user
            embed_submitted = discord.Embed(title="Submitted ✅", 
                                            description='Thank you for helping this community project!', 
                                            color=discord.Color.green())\
                    .set_author(name=author.display_name, icon_url=author.avatar_url)\
                    .set_footer(text='Your username, user id and server id has been submitted with the request.')
            await sentembed.delete()
            await ctx.send(embed=embed_submitted)

    @commands.command(description='Help Yuuto by giving us a suggestion or a bug report!',
                      help='This command will let you help Yuuto by giving it a suggestion or a bug report!', 
                      aliases=['suggestion'])
    async def suggest(self, ctx: commands.Context):
        author: discord.User = ctx.author
        embed = discord.Embed(title="Got a suggestion or bug report?", 
                              description="Don't hesitate to reach out to the developers in the [Project Yuuto](https://discord.gg/FAZaeBnxpz) discord server! "\
                                          "You can also create an issue on the bot's [GitHub page](https://github.com/Yuuto-Project/yuupy/) if you would prefer that!", 
                              color=0xFDBBE4)\
            .set_author(name=author.display_name, icon_url=author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
