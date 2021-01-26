from typing import List, Union

import discord

from src.events_handler.on_message.command import Command
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.utils.utils import get_role_id, get_channel_id, get_user_id


class UpdateCommand(Command):
    name: str = 'update'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Update command:\n\n",
                                               f"`{prefix}{UpdateCommand.name} CHAN_ID [[u]ROLE_ID[:PERM_GROUP]]+`\n"
                                               "Update a channel or a category. If PERM_GROUP is not given, the"
                                               " permission for this role are removed. Use `default` instead of"
                                               " ROLE_ID to set the default permission of the channel\n"
                                               "If the letter `u` is added before an id or a mention, it will be"
                                               " parsed as the a user id.")

    @staticmethod
    def get_description() -> str:
        return "update channel's permissions."

    @staticmethod
    async def update_user(channel: discord.abc.GuildChannel, user_arg: str,
                          perm_group: str, config: Config) -> Union[discord.Embed, None]:
        user_id = get_user_id(user_arg)
        if user_id == -1:
            return EmbedsManager.error_embed("Error\n", f"The user id `{user_arg}` is not valid.")
        member = await channel.guild.fetch_member(user_id)
        if not member:
            return EmbedsManager.error_embed("Error\n", f"The user `{user_id}` does not exists on this server")

        perm = None
        if perm_group != "":
            if perm_group not in config.guilds[channel.guild.id].keys():
                return EmbedsManager.error_embed("Unknown Permission Group",
                                                 f"The group {perm_group} does not exists on this server")
            perm = config.guilds[channel.guild.id][perm_group].permissions_overwrite
        await channel.set_permissions(member, overwrite=perm)
        return None

    @staticmethod
    async def update_role(channel: discord.abc.GuildChannel, role_arg: str,
                          perm_group: str, config: Config) -> Union[discord.Embed, None]:
        if role_arg == 'default':
            role = channel.guild.default_role
        else:
            role_id = get_role_id(role_arg)
            if role_id == -1:
                return EmbedsManager.error_embed("Error\n", f"The role id `{role_arg}` is not valid.")
            role = channel.guild.get_role(role_id)
            if not role:
                return EmbedsManager.error_embed("Error\n", f"The role `{role_arg}` does not exists on this server")

        perm = None
        if perm_group != "":
            if perm_group not in config.guilds[channel.guild.id].keys():
                return EmbedsManager.error_embed("Unknown Permission Group",
                                                 f"The group {perm_group} does not exists on this server")
            perm = config.guilds[channel.guild.id][perm_group].permissions_overwrite
        await channel.set_permissions(role, overwrite=perm)
        return None

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) == 1:
            return await message.channel.send(embed=UpdateCommand.get_help_msg(config.prefix))

        channel_id = get_channel_id(args[1])
        if channel_id == -1:
            return await message.channel.send(
                embed=EmbedsManager.error_embed("Error\n", f"The id `{args[1]}` is not valid."))
        else:
            channel = message.guild.get_channel(int(channel_id))
            if not channel:
                return await message.channel.send(
                    embed=EmbedsManager.error_embed("Error\n", f"The channel could not be found on this server."))

        for i in range(2, len(args)):
            arg = args[i].split(':', 1)
            if arg[0][0] == 'u':
                embed = await UpdateCommand.update_user(channel, arg[0][1:],
                                                        arg[1].upper() if len(arg) > 1 else "", config)
            else:
                embed = await UpdateCommand.update_role(channel, arg[0],
                                                        arg[1].upper() if len(arg) > 1 else "", config)

            if embed is not None:
                await message.channel.send(embed=embed)

        return await message.channel.send(embed=EmbedsManager.complete_embed("Success",
                                                                             "The channel "
                                                                             f"`{channel.name}({channel_id})`"
                                                                             "has been updated."))
