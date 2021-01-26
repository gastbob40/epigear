from typing import List, Dict
import os

import discord

from src.config_builder.config_builder import ConfigBuilder
from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.dump import DumpCommand
from src.models.permission_group import PermissionGroup
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.discord_creator.discord_creator import DiscordCreator


class LoadCommand(Command):
    name: str = 'load'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Loading configuration:\n\n",
                                               f"`{prefix}{LoadCommand.name} ROLE_LINK CHANNEL_LINK [ROLE_NAME]*`\n"
                                               "Load configuration files to add to the server. Both ROLE_LINK and"
                                               " CHANNEL_LINK must be links to configuration files accessible as"
                                               " raw data with pastebin for example. The format of these files is"
                                               " explained in the README of the project.\n"
                                               "If ROLE_NAMEs are given, those roles will be ignored during the"
                                               " creation of the roles, this allow the bot to set permissions in"
                                               " specific channels for some roles, but to not modify these roles"
                                               " in the default server settings.")

    @staticmethod
    def get_description() -> str:
        return "load configuration to build roles and channels."

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) < 3:
            return await message.channel.send(embed=LoadCommand.get_help_msg(config.prefix))
        role_link = args[1]
        channel_link = args[2]
        roles_to_ignore = []
        if len(args) > 3:
            roles_to_ignore = args[3:]
        creator = DiscordCreator(client, message.guild.id, config.guilds[message.guild.id], roles_to_ignore)
        try:
            await creator.create_all(role_link, channel_link)
            embed = EmbedsManager.complete_embed("Success", "Configuration as been updated on the server, "
                                                            f"use `{config.prefix}{DumpCommand.name}` to see it.")
        except Exception as e:
            embed = EmbedsManager.error_embed("Unexpected error during configuration loading", f"{e}")

        await message.channel.send(embed=embed)
