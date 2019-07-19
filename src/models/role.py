from src.models.permission import Permission
from discord.colour import Color


class Role:
    name: str
    color: Color
    permission: Permission
    hoist: bool
    mentionable: bool

    def __init__(self, name: str, color_code: int = 0x000000, permission: Permission = None,
                 hoist: bool = False, mentionable: bool = False):
        self.name = name
        self.color = Color(color_code)
        self.permissions = permission
        self.hoist = hoist
        self.mentionable = mentionable

