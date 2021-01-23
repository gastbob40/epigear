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
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) != 1:
            return await message.channel.send(embed=HelpCommand.get_help_msg(config.prefix))

        msg = f"Here is a list of commands available. Use `{config.prefix}<cmd> -h` " \
              "for more information about each commands.\n"
        for command in sorted(Command.__subclasses__(), key=lambda cmd: cmd.name):
            msg += f"`{config.prefix}{command.name}`\n"
        return await message.channel.send(embed=EmbedsManager.information_embed("Help", msg))
