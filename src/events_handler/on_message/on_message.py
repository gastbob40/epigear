import discord

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
            return

        if message.guild.id not in config.guilds.keys():
            await message.channel.send(
                embed=EmbedsManager.error_embed(
                    "Erreur",
                    f"Ce serveur n'est pas encore été configuré. "
                    f"Utilisez `{config.prefix}init -h` pour plus d'informations"
                )
            )
