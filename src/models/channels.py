from typing import Dict
from discord import Role as RoleDiscord
from discord import PermissionOverwrite

from src.utils import category_name_format


class Channel:
    name: str
    overwrites: Dict[RoleDiscord, PermissionOverwrite]
    default_perm: PermissionOverwrite
    topic: str

    def __init__(self, name: str, overwrites: Dict[RoleDiscord, PermissionOverwrite],
                 default_perm: PermissionOverwrite, topic: str = ""):
        self.name = name
        self.overwrites = overwrites
        self.default_perm = default_perm
        self.topic = topic


class Category(Channel):
    channels: Dict[str, Channel]
    vocal_channels: Dict[str, Channel]

    def __init__(self, name: str, overwrites: Dict[RoleDiscord, PermissionOverwrite], channels: Dict[str, Channel],
                 vocal_channels: Dict[str, Channel], default_perm: PermissionOverwrite):
        super().__init__(category_name_format(name), overwrites, default_perm)
        self.channels = channels
        self.vocal_channels = vocal_channels
