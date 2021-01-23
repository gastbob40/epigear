import discord
import logging
import re

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.init import InitCommand
from src.events_handler.on_message.commands import *
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager

# Logger
logger = logging.getLogger("epigear_logger")


class OnMessage:
    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, config: Config):
        if message.author.bot or isinstance(message.author, discord.User):
            return

        if message.content is None or not message.content.startswith(config.prefix):
            return

        args = re.split('[ \n\r]', message.content)
        cmd = args[0][len(config.prefix):].lower()

        if cmd != 'init' and message.guild.id not in config.guilds.keys():
            await message.channel.send(
                embed=EmbedsManager.error_embed(
                    "Error",
                    f"This server has not been configured yet. "
                    f"Use `{config.prefix}init -h` for more information"
                )
            )
            return

        for command in Command.__subclasses__():
            if command.name == cmd:
                logger.debug(f"Command {command.name}")

                if not command.has_permission(message.author):
                    logger.debug(f"Command {command.name}: Permission error")
                    embed = EmbedsManager.error_embed("Error\n", "You don't have the necessary permissions.")
                    return await message.channel.send(embed=embed)

                if len(args) > 1 and args[1] == '-h':
                    return await message.channel.send(embed=command.get_help_msg(config.prefix))

                return await command.handle(client, message, args, config)
