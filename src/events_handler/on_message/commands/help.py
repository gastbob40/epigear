from typing import List, Dict

import discord

from src.events_handler.on_message.command import Command
from src.models.permission_group import PermissionGroup
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager


class HelpCommand(Command):
    name: str = 'help'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Help commands:\n\n",
                                               f"`{prefix}{HelpCommand.name}`\n"
                                               "Display list of all commands")

    @staticmethod
    def get_description() -> str:
        return "display help message."

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) != 1:
            return await message.channel.send(embed=HelpCommand.get_help_msg(config.prefix))

        msg = f"Here is a list of commands available. Use `{config.prefix}<cmd> -h` " \
              "for more information about each command.\n"
        longest_desc = max([len(c.get_description()) for c in Command.__subclasses__()])
        longest_name = max([len(c.name) for c in Command.__subclasses__()]) + len(config.prefix)
        for command in sorted(Command.__subclasses__(), key=lambda cmd: cmd.name):
            msg += f"`{config.prefix}{command.name}".ljust(longest_name + 5)
            msg += f"{command.get_description()}`".rjust(longest_desc + 2)
            msg += "\n"
        return await message.channel.send(embed=EmbedsManager.information_embed("Help", msg))
