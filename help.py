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

    async def build_list_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]) -> str:
        prefix = os.getenv("PREFIX")
        result_string = 'Here is a list of all commands and their descriptions:\n\n'
        for item in mapping.items():
            result_string += '{} {}\n'.format(self.emoji_mapping[item[0].qualified_name], item[0].qualified_name) if item[0] is not None else '💡 No Category\n'
            cmds: List[commands.Command] = await self.filter_commands(commands=item[1], sort=True)
            deduplicated = sorted(set(cmds), key=lambda x: x.name)
            for cmd in deduplicated:
                result_string += '`{}` - {}\n'.format(cmd.name, cmd.description)
            result_string += '\n'
        return result_string

    def build_list_cog_help(self, cog: commands.Cog) -> str:
        result_string = f'{self.emoji_mapping[cog.qualified_name]} Here is a list of commands for `{cog.qualified_name}`\n'
        cmds: List[commands.Command] = sorted(cog.get_commands(), key=lambda x: x.name)
        for cmd in cmds:
            result_string += '`{}` - {}\n'.format(cmd.name, cmd.description)
        return result_string

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
        prefix = os.getenv("PREFIX")
        result = await self.build_list_bot_help(mapping)
        result += f"_The current prefix is `{prefix}` Usage example: `{prefix}ping`_"
        await self.context.send(result)

    # Help for each cog. List all available commands under that specific cog.
    async def send_cog_help(self, cog: commands.Cog):
        result = self.build_list_cog_help(cog)
        await self.context.send(result)

    # Help for each command. Showing the command's name, detailed description (help) and aliases.
    async def send_command_help(self, command: commands.Command):
        result = self.build_list_command_help(command)
        await self.context.send(result)
