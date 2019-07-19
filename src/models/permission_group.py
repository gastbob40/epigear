from typing import List

import discord


class PermissionGroup:
    name: str
    permissions: discord.Permissions

    def __init__(self, name: str):
        self.name = name
        self.permissions = discord.Permissions()

    def __str__(self):
        return self.name


