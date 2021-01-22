import discord

from src.events_handler.on_message.command import Command
from src.events_handler.on_message.commands.init import InitCommand
from src.utils.config import Config
from src.utils.embeds_manager import EmbedsManager


class OnMessage:
    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, config: Config):
        if message.author.bot or isinstance(message.author, discord.User):
            return

        if message.content and not message.content.startswith(config.prefix):
            return

        args = message.content.split(' ')
        cmd = args[0][len(config.prefix):].lower()

        if cmd == 'init':
            return await InitCommand.handle(client, message, args, config)

        if message.guild.id not in config.guilds.keys():
            await message.channel.send(
                embed=EmbedsManager.error_embed(
                    "Error",
                    f"This server has not been configured yet. "
                    f"Use `{config.prefix}init -h` for more information"
                )
            )

        for command in Command.__subclasses__():
            if command.name == cmd:
                return await command.handle(client, message, args, config)
