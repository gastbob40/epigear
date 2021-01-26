import os
from typing import List

import discord

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.init import InitCommand
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.yaml_parser.permissions_parser import PermissionGroupParser


class ClearConfigCommand(Command):
    name: str = 'clear_config'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Clear config command:\n\n",
                                               f"`{prefix}{InitCommand.name}`\n"
                                               "Clear the configuration of the server.")

    @staticmethod
    def get_description() -> str:
        return "clear the configuration of the server."

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) != 1:
            return await message.channel.send(embed=InitCommand.get_help_msg(config.prefix))

        name = f"{message.guild.id}.yml"
        file = discord.File(os.path.join(config.perm_group_path, name))
        embed = EmbedsManager.complete_embed("Success\n", "The configuration for this server has been removed, "
                                                          f"see `{config.prefix}{InitCommand.name} -h` "
                                                          "to create a new configuration.")
        config.guilds.pop(message.guild.id)
        await message.channel.send(embed=embed, file=file)
        os.remove(os.path.join(config.perm_group_path, name))
