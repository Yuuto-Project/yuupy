from discord.ext import commands
from typing import List, Mapping, Optional, Set, Union
import discord


class Help(commands.HelpCommand):
    def __init__(self, attributes: dict):
        super().__init__(command_attrs=attributes)
        self.color = discord.Colour(0xFDBBE4)

    # Override the general help (without any arguments)
    async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]):
        author: Union[discord.User, discord.Member] = self.context.author
        embed = discord.Embed(description='Here is a list of all commands and their descriptions:', color=self.color)
        embed.set_footer(
            text='Type y!help <command> for more info on a command.\nYou can also type y!help <category> for more info on a category.')
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        for item in mapping.items():
            # Get sorted command list of the cog the commands belong to
            cmds: List[commands.Command] = await self.filter_commands(commands=item[1], sort=True)
            # Deduplicate the command list so that we won't have repeated items
            cmds_deduplicated = set(cmds)
            cmd_names = []
            for cmd in cmds_deduplicated:
                cmd_names.append('`' + cmd.name + '`')
            cmd_string = ' '.join(cmd_names)
            category_name = 'No Category'
            if item[0] is not None:
                category_name = str(item[0].qualified_name)
            embed.add_field(name=category_name, value=cmd_string, inline=True)
        await self.context.send(embed=embed)

    # Help for each cog. List all available commands under that specific cog.
    async def send_cog_help(self, cog: commands.Cog):
        author: Union[discord.User, discord.Member] = self.context.author
        cmds: List[commands.Command] = cog.get_commands()
        cog_name = cog.qualified_name
        embed = discord.Embed(title=cog_name, description='Here is a list of commands for `' + cog_name + '`.', color=self.color)
        embed.set_footer(text='Type y!help <command> for more info on a command.')
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        for cmd in cmds:
            embed.add_field(name=cmd.name, value=cmd.description, inline=False)
        await self.context.send(embed=embed)

    # Help for each command. Showing the command's name, detailed description (help) and aliases.
    async def send_command_help(self, command: commands.Command):
        author: Union[discord.User, discord.Member] = self.context.author
        embed = discord.Embed(title=command.name, color=self.color, description=command.help)
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        if len(command.aliases) > 0:
            aliases = map(lambda x: '`' + x + '`', command.aliases)
            embed.add_field(name='Aliases', value=' '.join(aliases), inline=False)
        await self.context.send(embed=embed)
