import discord
from typing import List

from src.utils.config import Config


class Command:
    name: str

    @staticmethod
    def get_help_msg(prefix: str) -> discord.Embed:
        return discord.Embed()

    @staticmethod
    def get_description() -> str:
        return ""

    @staticmethod
    async def handle(client: discord.Client, message: discord.Message, args: List[str], config: Config):
        return

    @staticmethod
    async def has_permission(guild: discord.Guild, user: discord.User):
        member = await guild.fetch_member(user.id)
        if not member:
            return False
        return member.guild_permissions.administrator
