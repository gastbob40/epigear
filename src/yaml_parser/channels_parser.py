from src.models.channels import Channel, Category
from src.models.role import Role
from src.models.permission_group import PermissionGroup
from typing import Dict
import yaml


class ChannelParser:

    @staticmethod
    def yaml_to_objects(permissions_groups: Dict[str, PermissionGroup], roles: Dict[str, Role]) -> Dict[str, Role]:
        with open('run/config_server/server_channels.yml', 'r') as stream:
            data = yaml.safe_load(stream)

        categories = {}

        for category_name in data:
            channels = {}

            for channel_name in data[category_name]['channels']:
                new_channel = Channel(data[category_name]['channels'][channel_name]['name'],
                                      data[category_name]['channels'][channel_name]['overwrites'])
                channels[channel_name]=new_channel

            new_category = Category(data[category_name]['name'], data[category_name]['overwrites'], channels)
            categories[category_name] = new_category

        return roles
