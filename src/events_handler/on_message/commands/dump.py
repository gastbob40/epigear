from typing import List, Dict
import os

import discord

from src.config_builder.config_builder import ConfigBuilder
from src.events_handler.on_message.command import Command
from src.models.permission_group import PermissionGroup
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager


class DumpCommand(Command):
    name: str = 'dump'

    @staticmethod
    def all_groups(groups: Dict[str, PermissionGroup]) -> discord.Embed:
        groups_names = ""
        for g in sorted(groups.keys()):
            groups_names += f"- {g}\n"
        return EmbedsManager.complete_embed("Permission groups on the server:\n",
                                            groups_names)

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Dumping configuration:\n\n",
                                               f"`{prefix}{DumpCommand.name}`\n"
                                               "Dump the configuration of the server")

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) != 1:
            return await message.channel.send(embed=DumpCommand.all_groups(config.guilds[message.guild.id]))

        config_builder = ConfigBuilder(client, message.guild, config.guilds[message.guild.id], config.perm_group_path)
        config_builder.create_config()

        roles = discord.File(os.path.join(config.perm_group_path, f"{message.guild.id}_roles.yml"))
        channels = discord.File(os.path.join(config.perm_group_path, f"{message.guild.id}_channels.yml"))
        perm_groups = discord.File(os.path.join(config.perm_group_path, f"{message.guild.id}.yml"))

        embed = EmbedsManager.complete_embed("Config", "Here is the configuration files for the server "
                                                       f"`{message.guild.name}({message.guild.id})`")
        await message.channel.send(embed=embed, files=[roles, channels, perm_groups])

        os.remove(os.path.join(config.perm_group_path, f"{message.guild.id}_roles.yml"))
        os.remove(os.path.join(config.perm_group_path, f"{message.guild.id}_channels.yml"))
