from typing import List, Dict
import re

import discord

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.get_perm_group import GetPermGroupCommand
from src.models.permission_group import PermissionGroup
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.utils.utils import str_to_bool


class AddPermGroupCommand(Command):
    name: str = 'add_perm_group'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Adding permission groups:\n\n",
                                               f"`{prefix}{AddPermGroupCommand.name} PERM_GROUP [PERM:VALUE]*`\n"
                                               "Add a permission group. The name must match the pattern `[A-Z_]*`"
                                               ", and it must not be named UNKNOWN.\n"
                                               f"`{prefix}{AddPermGroupCommand.name} -p`\n"
                                               "Print a list of all the possible permissions")

    @staticmethod
    def get_description() -> str:
        return "add permission group."

    @staticmethod
    def get_all_perm() -> discord.Embed:
        perm_names = ""
        for k, v in sorted(iter(discord.Permissions.all())):
            perm_names += f"{k}:{v}\n"
        return EmbedsManager.complete_embed("Possible permission for a permission group:\n", perm_names)

    @staticmethod
    def new_perm(name: str, args: List[str]) -> PermissionGroup:
        perm = PermissionGroup(name)
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
            return await message.channel.send(embed=AddPermGroupCommand.get_help_msg(config.prefix))

        if args[1] == '-p':
            return await message.channel.send(embed=AddPermGroupCommand.get_all_perm())

        name = args[1].upper()
        pattern = re.compile("^[0-9A-Z_]+$")
        if not pattern.match(name) or name == 'UNKNOWN':
            embed = EmbedsManager.error_embed("Error\n", f"The name `{name}` is not valid for a perm group, "
                                                         f"see `{config.prefix}{AddPermGroupCommand.name} -h`.")
            return await message.channel.send(embed=embed)

        if name in config.guilds[message.guild.id].keys():
            embed = EmbedsManager.error_embed("Error\n", f"The perm group `{name}` already exists on this server, "
                                                         f"use `{config.prefix}TODO` "
                                                         f"to update it.")
            return await message.channel.send(embed=embed)

        config.guilds[message.guild.id][name] = AddPermGroupCommand.new_perm(name, args)

        embed = EmbedsManager.complete_embed("Success\n", "The permission group has been added to the "
                                                          "configuration of for this server, "
                                                          f"use `{config.prefix}{GetPermGroupCommand.name} -h` "
                                                          "to check the permissions.")
        await message.channel.send(embed=embed)
        config.dump_perm_group(message.guild.id)
