from src.models.channels import Channel, Category
from src.models.role import Role
from src.models.permission_group import PermissionGroup
from typing import Dict
from discord import Role as RoleDiscord
from discord import PermissionOverwrite
import yaml


class ChannelParser:

    @staticmethod
    def yaml_to_objects(permissions_groups: Dict[str, PermissionGroup], roles: Dict[str, Role]) -> Dict[str, Category]:
        with open('run/config_server/server_channels.yml', 'r') as stream:
            data = yaml.safe_load(stream)

        categories = {}

        for category_name in data:
            channels = {}

            for channel_name in data[category_name]['channels']:
                overwrites = ChannelParser.__overwrites_parser__(
                    data[category_name]['channels'][channel_name]['overwrites'], permissions_groups, roles)
                new_channel = Channel(data[category_name]['channels'][channel_name]['name'], overwrites)
                channels[channel_name] = new_channel

            overwrites = ChannelParser.__overwrites_parser__(
                data[category_name]['overwrites'], permissions_groups, roles)
            new_category = Category(data[category_name]['name'], overwrites, channels)
            categories[category_name] = new_category

        return categories

    @staticmethod
    def __overwrites_parser__(raw_overwrites: Dict[str, str],permissions_groups: Dict[str, PermissionGroup],
                            roles: Dict[str, Role]) -> Dict[RoleDiscord, PermissionOverwrite]:

        overwrites = {}

        for role_name in raw_overwrites:
            role_discord = roles[role_name].role_discord
            perm = permissions_groups[raw_overwrites[role_name]].permissions_overwrite
            overwrites[role_discord] = perm

        return overwrites
