from typing import Dict
from discord import Role as RoleDiscord
from discord import PermissionOverwrite


class Channel:
    name: str
    overwrites: Dict[RoleDiscord, PermissionOverwrite]

    def __init__(self, name: str, overwrites: Dict[RoleDiscord, PermissionOverwrite]):
        self.name = name
        self.overwrites = overwrites


class Category(Channel):
    channels: Dict[str, Channel]
    vocal_channels: Dict[str, Channel]

    def __init__(self, name: str, overwrites: Dict[RoleDiscord, PermissionOverwrite], channels: Dict[str, Channel],
                 vocal_channels: Dict[str, Channel]):
        super().__init__(name, overwrites)
        self.channels = channels
        self.vocal_channels = vocal_channels
