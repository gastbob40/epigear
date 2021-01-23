import re
from typing import List

import discord

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.init import InitCommand
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.utils.utils import get_perm_overwrite_group


class InspectCommand(Command):
    name: str = 'inspect'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Inspect command:\n\n",
                                               f"`{prefix}{InspectCommand.name} [ID[:ROLE_ID]]+`\n"
                                               "Inspect a channel or a category. If a role ID is given, the detail of"
                                               " the permission will be displayed for the role and not just the"
                                               " permission group for the role.")

    @staticmethod
    def inspect_role_in_channel(channel: discord.abc.GuildChannel, chan_id: int, role_id: int,
                                config: Config) -> discord.Embed:

        role = channel.guild.get_role(role_id)
        if not role:
            return EmbedsManager.error_embed("Error\n", f"The role does not exists on this server")

        info = f"The role `{role.name}({role_id})` does not have specific permission " \
               f"in the channel `{channel.name}({chan_id})`"

        for role, perm in channel.overwrites.items():
            if role.id != role_id:
                continue
            info = f"The role `{role.name}({role_id})` has the permission group" \
                   f" `{get_perm_overwrite_group(config.guilds[channel.guild.id], perm)}`" \
                   f" in the channel `{channel.name}({chan_id})`\n"
            info += '\n'.join(sorted([f"`{p}:{v}`" for p, v in iter(perm) if v is not None]))
        return EmbedsManager.complete_embed("Success\n", info)

    @staticmethod
    def inspect_all_role_in_channel(channel: discord.abc.GuildChannel, chan_id: int, config: Config) -> discord.Embed:

        default = get_perm_overwrite_group(config.guilds[channel.guild.id],
                                           channel.overwrites_for(channel.guild.default_role))
        info = f"The default permission group for the channel {channel.name}({chan_id}) is\n`{default}`\n" \
               f"The others permission groups for this channel are :\n"

        for role, perm in channel.overwrites.items():
            prefix = f"Role {role.name}: {role.id}" if type(role) == discord.Role else \
                f"User {role.display_name}: {role.id}"
            if role.name == "@everyone":
                continue
            info += f"`{prefix}:{get_perm_overwrite_group(config.guilds[channel.guild.id], perm)}`\n"
        return EmbedsManager.complete_embed("Success\n", info)

    @staticmethod
    def inspect_channel(chan_id: str, role_id: str, message: discord.Message, config: Config) -> discord.Embed:
        pattern = re.compile("^[0-9]+$")
        if not pattern.match(chan_id):
            return EmbedsManager.error_embed("Error\n", f"The id `{chan_id}` is not valid.")
        else:
            chan = message.guild.get_channel(int(chan_id))
            if not chan:
                return EmbedsManager.error_embed("Error\n", f"The channel could not be found on this server.")

        if role_id != "":
            if not pattern.match(role_id):
                return EmbedsManager.error_embed("Error\n", f"The role id `{role_id}` is not valid.")
            return InspectCommand.inspect_role_in_channel(chan, int(chan_id), int(role_id), config)
        return InspectCommand.inspect_all_role_in_channel(chan, int(chan_id), config)

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        if len(args) == 1:
            return await message.channel.send(embed=InspectCommand.get_help_msg(config.prefix))

        for i in range(1, len(args)):
            arg = args[i].split(':', 1)
            embed = InspectCommand.inspect_channel(arg[0], arg[1] if len(arg) > 1 else "", message, config)
            await message.channel.send(embed=embed)
