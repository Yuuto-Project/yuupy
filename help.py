from discord.ext import commands
from typing import List, Mapping, Optional, Set, Union
import discord
import os


class Help(commands.HelpCommand):
    def __init__(self, attributes: dict):
        super().__init__(command_attrs=attributes)
        self.prefix = os.getenv('PREFIX')
        self.emoji_mapping = {
            'Utility': '⚙️',
            'Info': 'ℹ️',
            'Fun': '🎲',
            'No Category': '💡'
        }

    # This function builds the text for the help (list) command (ex: y!help)
    async def build_list_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]) -> str:
        result_string = 'Here is a list of all commands and their descriptions:\n\n'

        # For every type (cog) of command (Utility, Info, Fun)
        for item in mapping.items():
            # If it has a type, add an entry for it
            if item[0] is not None:
                result_string += f'{self.emoji_mapping[item[0].qualified_name]} {item[0].qualified_name} \n'
            else:
                result_string += f'{self.emoji_mapping["No Category"]} No Category \n'

            # Get every command and their details from the cogs and then sort them
            cmds: List[commands.Command] = await self.filter_commands(commands=item[1], sort=True)
            deduplicated = sorted(set(cmds), key=lambda x: x.name)

            # For every command; add them to the list
            for cmd in deduplicated:
                result_string += f'`{cmd.name}` - {cmd.description}\n'
            result_string += '\n'
        return result_string

    # This function builds the text for the help [cog] command (ex: y!help Utility)
    def build_list_cog_help(self, cog: commands.Cog) -> str:
        result_string = f'{self.emoji_mapping[cog.qualified_name]} Here is a list of commands in the `{cog.qualified_name}` category\n'

        cmds: List[commands.Command] = sorted(cog.get_commands(), key=lambda x: x.name)
        for cmd in cmds:
            result_string += f'`{cmd.name}` - {cmd.description}\n'
        return result_string

    # This function builds the text for the help [command] command (ex: y!help ping)
    def build_list_command_help(self, command: commands.Command) -> str:
        if command.cog is not None:
            result_string = f'**Category:** {self.emoji_mapping[command.cog.qualified_name]} {command.cog.qualified_name}\n'
        else:
           result_string = f'**Category:** {self.emoji_mapping["No Category"]} No Category \n'

        # Signiture = Default generated usage or overwritten by the usage='' parameter
        if command.signature is not None and len(command.signature) > 0:
            result_string += f'**Usage:** `{self.prefix}{command.name} {command.signature}`\n'
        else:
            result_string += f'**Usage:** `{self.prefix}{command.name}`\n'

        # Note: help='' parameter is used for the detailed help command, list uses the shorter description=''
        if command.help is not None and len(command.help) > 0: 
            result_string += f'**Description:** {command.help}\n'
        # This should only be used as a fallback and help='' should always be defined.
        elif command.description is not None and len(command.description) > 0:
            result_string += f'**Description:** {command.description}\n'

        # If there are any aliases, list them
        if command.aliases is not None and len(command.aliases) > 0:
            aliases = list(map(lambda x: f'`{x}`', command.aliases))
            result_string += '**Aliases:** {}'.format(', '.join(aliases))
        return result_string

    # Override the Discord.py built in general help (the one without any arguments)
    async def send_bot_help(self, mapping: Mapping[Optional[commands.Cog], List[commands.Command]]):
        result = await self.build_list_bot_help(mapping)
        result += f"_The current prefix is `{self.prefix}` Usage example: `{self.prefix}ping`_"
        await self.context.send(result)

    # Help for each cog. List all available commands under that specific cog.
    async def send_cog_help(self, cog: commands.Cog):
        result = self.build_list_cog_help(cog)
        result += f"\n_The current prefix is `{self.prefix}` Usage example: `{self.prefix}ping`_"
        await self.context.send(result)

    # Help for each command. Showing the command's name, detailed description (help) and aliases.
    async def send_command_help(self, command: commands.Command):
        result = self.build_list_command_help(command)
        await self.context.send(result)
