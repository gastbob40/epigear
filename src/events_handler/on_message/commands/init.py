import os
from typing import List

import discord

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.get_perm_group import GetPermGroupCommand
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager
from src.yaml_parser.permissions_parser import PermissionGroupParser


class InitCommand(Command):
    name: str = 'init'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("Init command:\n\n",
                                               f"`{prefix}{InitCommand.name} <mod>`\n"
                                               "Init the permission groups for the server."
                                               "Use one of the following mods:\n"
                                               "- default : default perm groups\n"
                                               "- none : no perm group\n"
                                               "- file : use file uploaded with the command\n"
                                               f"`{prefix}{InitCommand.name} -h`\n"
                                               "Display this message.")

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):

        if message.guild.id in config.guilds.keys():
            embed = EmbedsManager.error_embed("Error\n", "This server has already been "
                                                         f"configured, use `{config.prefix}{GetPermGroupCommand.name}` "
                                                         f"to check the configuration")
            return await message.channel.send(embed=embed)

        if len(args) != 2 or args[1] not in ["default", "none", "file"]:
            return await message.channel.send(embed=InitCommand.get_help_msg(config.prefix))

        if args[1] == 'default':
            default = PermissionGroupParser.get_permissions_from_file(os.path.join(config.perm_group_path,
                                                                                   "default_perm_groups.yml"))
            config.guilds[message.guild.id] = default
        elif args[1] == 'none':
            config.guilds[message.guild.id] = dict()
        else:
            # TODO: add file with pastebin
            return
        config.dump_perm_group(message.guild.id)
        embed = EmbedsManager.complete_embed("Success\n", "This server has been configured, "
                                                          f"use `{config.prefix}get_perm_group` "
                                                          "to check the configuration")
        return await message.channel.send(embed=embed)
