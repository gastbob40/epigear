from typing import List, Union

import discord

from src.events_handler.on_message.command import Command
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.utils.utils import get_role_id, get_channel_id, get_user_id


class UpdateRoleCommand(Command):
    name: str = 'update_role'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Update Role command:\n\n",
                                               f"`{prefix}{UpdateRoleCommand.name} [ROLE_ID:PERM_GROUP]+`\n"
                                               "Update default perm of a role on the server. Use `default` instead of "
                                               "the role id to change the permissions of the role everyone.")

    @staticmethod
    async def update_role(guild: discord.Guild, role_arg: str,
                          perm_group: str, config: Config) -> Union[discord.Embed, None]:
        if role_arg == 'default':
            role = guild.default_role
        else:
            role_id = get_role_id(role_arg)
            if role_id == -1:
                return EmbedsManager.error_embed("Error\n", f"The role id `{role_arg}` is not valid.")
            role = guild.get_role(role_id)
            if not role:
                return EmbedsManager.error_embed("Error\n", f"The role `{role_arg}` does not exists on this server")

        perm = None
        if perm_group != "":
            if perm_group not in config.guilds[guild.id].keys():
                return EmbedsManager.error_embed("Unknown Permission Group",
                                                 f"The group {perm_group} does not exists on this server")
            perm = config.guilds[guild.id][perm_group].permissions
        await role.edit(permissions=perm)
        return None

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) == 1:
            return await message.channel.send(embed=UpdateRoleCommand.get_help_msg(config.prefix))

        for i in range(1, len(args)):
            arg = args[i].split(':', 1)
            if len(arg) != 2:
                await message.channel.send(embed=EmbedsManager.error_embed("Argument Error",
                                                                           "Wrong format for the "
                                                                           f"argument `{args[i]}`"))
                continue
            embed = await UpdateRoleCommand.update_role(message.guild, arg[0],
                                                        arg[1].upper(), config)
            if embed is not None:
                await message.channel.send(embed=embed)

        return await message.channel.send(embed=EmbedsManager.complete_embed("Success",
                                                                             "All roles have been updated"))
