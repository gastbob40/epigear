import discord
from typing import List

from src.utils.config import Config


class Command:
    name: str

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return discord.Embed()

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        return

    @staticmethod
    def has_permission(user: discord.User):
        return user.id == 277096487467352065
