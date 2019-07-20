from typing import Dict
from discord import Role as RoleDiscord
from discord import PermissionOverwrite


class Channel:
    name: str
    overwrites: Dict[RoleDiscord, PermissionOverwrite]
    default_perm: PermissionOverwrite

    def __init__(self, name: str, overwrites: Dict[RoleDiscord, PermissionOverwrite],
                 default_perm: PermissionOverwrite):
        self.name = name
        self.overwrites = overwrites
        self.default_perm = default_perm


class Category(Channel):
    channels: Dict[str, Channel]
    vocal_channels: Dict[str, Channel]

    def __init__(self, name: str, overwrites: Dict[RoleDiscord, PermissionOverwrite], channels: Dict[str, Channel],
                 vocal_channels: Dict[str, Channel], default_perm: PermissionOverwrite):
        super().__init__(name, overwrites, default_perm)
        self.channels = channels
        self.vocal_channels = vocal_channels
