from typing import List

import discord


class PermissionGroup:
    name: str
    permissions: discord.Permissions
    permissions_overwrite: discord.PermissionOverwrite

    def __init__(self, name: str):
        self.name = name
        self.permissions = discord.Permissions()
        self.permissions_overwrite = discord.PermissionOverwrite()

    def __str__(self):
        return self.name


