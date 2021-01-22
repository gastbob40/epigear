from typing import List, Dict

import discord

from src.events_handler.on_message.command import Command
from src.models.permission_group import PermissionGroup
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager


class GetPermGroupCommand(Command):
    name: str = 'get_perm_group'

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
                                               f"`{prefix}{GetPermGroupCommand.name} [-v] [group]`\n"
                                               "Display information about the permission group. Or"
                                               "display the list of all permission groups if no argument is given.\n"
                                               "If `-v` is given before the perm groups, all permission (even those"
                                               " set to None) will be displayed")

    @staticmethod
    def group_info(group: str, groups: Dict[str, PermissionGroup], verbose: bool):
        if group not in groups:
            embed = EmbedsManager.error_embed("Unknown Permission Group",
                                              f"The group {group} does not exists on this server")
        else:
            perm_names = ""
            for p, v in groups[group].permissions_overwrite:
                if v is None and not verbose:
                    continue
                perm_names += f"- {p} : {v}\n"
            embed = EmbedsManager.complete_embed(f"Permissions for group {group} on the server:\n",
                                                 perm_names)
        return embed

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if not Command.has_permission(message.author):
            return

        if len(args) > 1 and args[1] == '-h':
            return await message.channel.send(embed=GetPermGroupCommand.get_help_msg(config.prefix))

        if len(args) == 1:
            return await message.channel.send(embed=GetPermGroupCommand.all_groups(config.guilds[message.guild.id]))

        first = 1
        verbose = False
        if args[1] == '-v':
            first += 1
            verbose = True

        for i in range(first, len(args)):
            await message.channel.send(
                embed=GetPermGroupCommand.group_info(args[i], config.guilds[message.guild.id], verbose))
