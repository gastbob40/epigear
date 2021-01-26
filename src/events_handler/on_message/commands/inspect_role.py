import re
from typing import List, Dict

import discord

from src.events_handler.on_message.command import Command
from src.models.permission_group import PermissionGroup
from src.events_handler.on_message.commands.init import InitCommand
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.utils.utils import get_perm_group, get_channel_id, get_role_id


class InspectRolesCommand(Command):
    name: str = 'inspect_role'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Getting roles permissions:\n\n",
                                               f"`{prefix}{InspectRolesCommand.name} [-v] [ROLE_ID]+`\n"
                                               "Display permissions about the role. Or"
                                               "display the list of the permissions of all roles"
                                               "if no argument is given.\n"
                                               "If `-v` is given before the roles, all permission will be "
                                               "displayed for each roles and not juste the perm group")

    @staticmethod
    async def all_roles(guild: discord.Guild, perm_groups: Dict[str, PermissionGroup]) -> List[discord.Embed]:
        roles_perm = ""
        roles = await guild.fetch_roles()
        out = []
        l = 0
        for r in roles:
            v = f"`{r.name}: {r.id}:{get_perm_group(perm_groups, r.permissions)}`\n"
            if l + len(v) >= 2048:
                out.append(EmbedsManager.complete_embed("Permission groups for the roles on the server:\n",
                                                        roles_perm))
                roles_perm = ""
                l = 0
            roles_perm += v
            l += len(v)
        out.append(EmbedsManager.complete_embed("Permission groups for the roles on the server:\n",
                                                roles_perm))
        return out

    @staticmethod
    async def inspect_role(role_arg: str, guild: discord.Guild, perm_groups: Dict[str, PermissionGroup],
                           verbose: bool) -> discord.Embed:
        if role_arg == 'default':
            role = guild.default_role
        else:
            role_id = get_role_id(role_arg)
            if role_id == -1:
                return EmbedsManager.error_embed("Error\n", f"The role id `{role_arg}` is not valid.")
            role = guild.get_role(role_id)
            if role is None:
                return EmbedsManager.error_embed("Error\n", f"The role `{role_arg}` does not exists on this server")

        role_perm = f"`{role.name}: {role.id}:{get_perm_group(perm_groups, role.permissions)}`\n"
        if not verbose:
            return EmbedsManager.complete_embed(f"Permissions for the role {role.name}:", role_perm)

        for k, v in role.permissions:
            if v is None:
                continue
            role_perm += f"  `{k}:{v}`\n"
        return EmbedsManager.complete_embed(f"Permissions for the role {role.name}:",
                                            role_perm)

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) == 1:
            embeds = await InspectRolesCommand.all_roles(message.guild, config.guilds[message.guild.id])
            for e in embeds:
                await message.channel.send(embed=e)
            return

        first = 1
        verbose = False
        if args[1] == '-v':
            first += 1
            verbose = True

        for i in range(first, len(args)):
            embed = await InspectRolesCommand.inspect_role(args[i], message.guild,
                                                           config.guilds[message.guild.id], verbose)

            await message.channel.send(embed=embed)
