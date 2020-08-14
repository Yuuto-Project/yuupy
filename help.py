from discord.ext import commands
from typing import List, Mapping, Optional, Set, Union
import discord
import os


class Help(commands.HelpCommand):
    def __init__(self, attributes: dict):
        super().__init__(command_attrs=attributes)
        self.color = discord.Colour(0xFDBBE4)
        self.emoji_mapping = {
            'Utility': '⚙️',
            'Info': 'ℹ️',
            'Fun': '🎲'
        }

    async def build_embed_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]) -> discord.Embed:
        author: Union[discord.User, discord.Member] = self.context.author
        embed = discord.Embed(description='Here is a list of all commands and their descriptions:', color=self.color)
        embed.set_footer(
            text='Type y!help <command> for more info on a command.\nYou can also type y!help <category> for more info on a category.')
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        for item in mapping.items():
            # Get sorted command list of the cog the commands belong to
            cmds: List[commands.Command] = await self.filter_commands(commands=item[1], sort=True)
            # Deduplicate the command list so that we won't have repeated items
            cmds_deduplicated = sorted(set(map(lambda x: x.name, cmds)))
            cmd_names = []
            for cmd in cmds_deduplicated:
                cmd_names.append('`' + cmd + '`')
            cmd_string = ' '.join(cmd_names)
            category_name = 'No Category'
            if item[0] is not None:
                category_name = str(item[0].qualified_name)
            embed.add_field(name=category_name, value=cmd_string, inline=True)
        return embed

    async def build_list_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]) -> str:
        result_string = 'Here is a list of all commands and their descriptions:\n\n'
        for item in mapping.items():
            result_string += '{} {}\n'.format(self.emoji_mapping[item[0].qualified_name], item[0].qualified_name) if item[0] is not None else '💡 No Category\n'
            cmds: List[commands.Command] = await self.filter_commands(commands=item[1], sort=True)
            deduplicated = sorted(set(cmds), key=lambda x: x.name)
            for cmd in deduplicated:
                result_string += '`{}` - {}\n'.format(cmd.name, cmd.description)
            result_string += '\n'
        return result_string

    def build_embed_cog_help(self, cog: commands.Cog) -> discord.Embed:
        author: Union[discord.User, discord.Member] = self.context.author
        cmds: List[commands.Command] = cog.get_commands()
        cog_name = cog.qualified_name
        embed = discord.Embed(title=cog_name, description='Here is a list of commands for `' + cog_name + '`.',
                              color=self.color)
        embed.set_footer(text='Type y!help <command> for more info on a command.')
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        cmds = sorted(cmds, key=lambda x: x.name)
        for cmd in cmds:
            embed.add_field(name=cmd.name, value=cmd.description, inline=False)
        return embed

    def build_list_cog_help(self, cog: commands.Cog) -> str:
        result_string = f'{self.emoji_mapping[cog.qualified_name]} Here is a list of commands for `{cog.qualified_name}`\n'
        cmds: List[commands.Command] = sorted(cog.get_commands(), key=lambda x: x.name)
        for cmd in cmds:
            result_string += '`{}` - {}\n'.format(cmd.name, cmd.description)
        return result_string

    def build_embed_command_help(self, command: commands.Command) -> discord.Embed:
        author: Union[discord.User, discord.Member] = self.context.author
        embed = discord.Embed(title=command.name, color=self.color, description=command.help)
        embed.set_author(name=author.display_name, icon_url=author.avatar_url)
        if len(command.aliases) > 0:
            aliases = map(lambda x: '`' + x + '`', command.aliases)
            embed.add_field(name='Aliases', value=' '.join(aliases), inline=False)
        return embed

    def build_list_command_help(self, command: commands.Command) -> str:
        result_string = '**Category:** {} {}\n'.format(self.emoji_mapping[command.cog.qualified_name], command.cog.qualified_name) if command.cog is not None else '**Category:** 💡 No Category\n'
        if command.signature is not None and len(command.signature) > 0:
            result_string += '**Usage:** `{}{} {}`\n'.format(os.getenv('PREFIX'), command.name, command.signature)
        else:
            result_string += '**Usage:** `{}{}`\n'.format(os.getenv('PREFIX'), command.name)
        result_string += '**Description:** {}\n'.format(command.help)
        if len(command.aliases) > 0:
            aliases = list(map(lambda x: '`{}`'.format(x), command.aliases))
            result_string += '**Aliases:** {}'.format(', '.join(aliases))
        return result_string

    # Override the general help (without any arguments)
    async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]):
        if int(os.getenv('EMBED_HELP')) == 1:
            embed = await self.build_embed_bot_help(mapping)
            await self.context.send(embed=embed)
        else:
            result = await self.build_list_bot_help(mapping)
            await self.context.send(result)

    # Help for each cog. List all available commands under that specific cog.
    async def send_cog_help(self, cog: commands.Cog):
        if int(os.getenv('EMBED_HELP')) == 1:
            embed = self.build_embed_cog_help(cog)
            await self.context.send(embed=embed)
        else:
            result = self.build_list_cog_help(cog)
            await self.context.send(result)

    # Help for each command. Showing the command's name, detailed description (help) and aliases.
    async def send_command_help(self, command: commands.Command):
        if int(os.getenv('EMBED_HELP')) == 1:
            embed = self.build_embed_command_help(command)
            await self.context.send(embed=embed)
        else:
            result = self.build_list_command_help(command)
            await self.context.send(result)
