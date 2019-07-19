from src.models.permission import Permission
from discord import colour


class Role:
    name: str
    color: colour
    permission: Permission
    hoist: bool
    mentionable: bool

    def __init__(self, name: str, color_code: int = 0x000000, permission: Permission = None,
                 hoist: bool = False, mentionable: bool = False):
        self.name = name
        self.color = colour.Color(color_code)
        self.permissions = permission
        self.hoist = hoist
        self.mentionable = mentionable

