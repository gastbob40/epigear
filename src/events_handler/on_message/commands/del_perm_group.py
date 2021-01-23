from typing import List, Dict

import discord

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.get_perm_group import GetPermGroupCommand
from src.models.permission_group import PermissionGroup
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager


class DelPermGroupCommand(Command):
    name: str = 'del_perm_group'

    @staticmethod
    def all_groups(groups: Dict[str, PermissionGroup]) -> discord.Embed:
        groups_names = ""
        for g in sorted(groups.keys()):
            groups_names += f"- {g}\n"
        return EmbedsManager.complete_embed("Permission groups on the server:\n",
                                            groups_names)

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Getting permission groups:\n\n",
                                               f"`{prefix}{DelPermGroupCommand.name} PERM_GROUP`\n"
                                               "Remove the permission group from the configuration")

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) == 1:
            return await message.channel.send(embed=DelPermGroupCommand.all_groups(config.guilds[message.guild.id]))

        name = args[1].upper()

        if name not in config.guilds[message.guild.id].keys():
            embed = EmbedsManager.error_embed("Error\n", f"The perm group `{name}` does not exists on this server, "
                                                         f"use `{config.prefix}{DelPermGroupCommand.name}` "
                                                         f"to create it.")
            return await message.channel.send(embed=embed)

        config.guilds[message.guild.id].pop(name)
        embed = EmbedsManager.complete_embed("Success\n", "The permission group has been removed.")
        await message.channel.send(embed=embed)
        config.dump_perm_group(message.guild.id)
