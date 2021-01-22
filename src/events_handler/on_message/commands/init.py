import discord
from typing import List

from src.events_handler.on_message.command import Command
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager


class InitCommand(Command):
    name: str = 'init'

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return EmbedsManager.information_embed("**Init command:**\n\n",
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
        if not Command.has_permission(message.author):
            return

        if len(args) > 1 and args[1] == '-h':
            return await message.channel.send(embed=InitCommand.get_help_msg(config.prefix))
