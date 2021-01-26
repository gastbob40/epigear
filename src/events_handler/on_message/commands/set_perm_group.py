from typing import List, Dict
import re

import discord

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.get_perm_group import GetPermGroupCommand
from src.events_handler.on_message.commands.add_perm_group import AddPermGroupCommand
from src.models.permission_group import PermissionGroup
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.utils.utils import str_to_bool


class SetPermGroupCommand(Command):
    name: str = 'set_perm_group'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Adding permission groups:\n\n",
                                               f"`{prefix}{SetPermGroupCommand.name} PERM_GROUP [PERM:VALUE]*`\n"
                                               "Set some permission to an existing permission group.\n"
                                               f"`{prefix}{SetPermGroupCommand.name} -p`\n"
                                               "Print a list of all the possible permissions")

    @staticmethod
    def get_description() -> str:
        return "add permission to permission group."

    @staticmethod
    def get_all_perm() -> discord.Embed:
        perm_names = ""
        for k, v in sorted(iter(discord.Permissions.all())):
            perm_names += f"{k}:{v}\n"
        return EmbedsManager.complete_embed("Possible permission for a permission group:\n", perm_names)

    @staticmethod
    def update_perm(perm: PermissionGroup, args: List[str]):
        values: Dict[str, bool] = dict()
        for i in range(2, len(args)):
            perm_value = args[i].split(':')
            if len(perm_value) != 2:
                continue
            values[perm_value[0]] = str_to_bool(perm_value[1])
        perm.permissions.update(**values)
        perm.permissions_overwrite.update(**values)
        return perm

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):

        if len(args) == 1:
            return await message.channel.send(embed=SetPermGroupCommand.get_help_msg(config.prefix))

        if args[1] == '-p':
            return await message.channel.send(embed=SetPermGroupCommand.get_all_perm())

        name = args[1].upper()

        if name not in config.guilds[message.guild.id].keys():
            embed = EmbedsManager.error_embed("Error\n", f"The perm group `{name}` does not exists on this server, "
                                                         f"use `{config.prefix}{AddPermGroupCommand.name}` "
                                                         f"to create it.")
            return await message.channel.send(embed=embed)

        SetPermGroupCommand.update_perm(config.guilds[message.guild.id][name], args)

        embed = EmbedsManager.complete_embed("Success\n", "The permission group has been modified, "
                                                          f"use `{config.prefix}{GetPermGroupCommand.name} -h` "
                                                          "to check the permissions.")
        await message.channel.send(embed=embed)
        config.dump_perm_group(message.guild.id)
