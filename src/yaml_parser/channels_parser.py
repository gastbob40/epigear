from typing import Dict
from discord import Role as RoleDiscord
from discord import PermissionOverwrite
import yaml
import logging

from src.models.channels import Channel, Category
from src.models.role import Role
from src.models.permission_group import PermissionGroup
from src.utils import channel_name_format

logger = logging.getLogger()


class ChannelParser:

    @staticmethod
    def yaml_to_objects(permissions_groups: Dict[str, PermissionGroup], roles: Dict[str, Role]) -> Dict[str, Category]:
        with open('run/config_server/server_channels.yml', 'r', encoding='utf8') as stream:
            data = yaml.safe_load(stream)
        logger.info('Get categories from config')

        categories = {}

        for category_name in data:
            logger.debug('Parsing category {}'.format(category_name))

            # Text Channels
            channels = ChannelParser.__get_channels__(data[category_name]['channels'], permissions_groups, roles)

            # Vocal Channels
            vocal_channels = ChannelParser.__get_channels__(data[category_name]['vocal_channels'],
                                                            permissions_groups, roles)

            overwrites = {} if not data[category_name]['overwrites'] else \
                ChannelParser.__overwrites_parser__(data[category_name]['overwrites'], permissions_groups, roles)

            default_perm = permissions_groups[data[category_name]['default_perm']].permissions_overwrite

            new_category = Category(data[category_name]['name'], overwrites, channels, vocal_channels, default_perm)
            categories[category_name] = new_category

        logger.info('{} categories parsed'.format(len(data)))

        return categories

    @staticmethod
    def __overwrites_parser__(raw_overwrites: Dict[str, str], permissions_groups: Dict[str, PermissionGroup],
                              roles: Dict[str, Role]) -> Dict[RoleDiscord, PermissionOverwrite]:
        overwrites = {}

        for role_name in raw_overwrites:
            role_discord = roles[role_name].role_discord
            perm = permissions_groups[raw_overwrites[role_name]].permissions_overwrite
            overwrites[role_discord] = perm

        return overwrites

    @staticmethod
    def __get_channels__(channels_info, permissions_groups: Dict[str, PermissionGroup],
                         roles: Dict[str, Role]) -> Dict[str, Channel]:
        if channels_info is None:
            return {}

        channels = {}

        for channel_name in channels_info:
            logger.debug('Parsing channel {}'.format(channel_name))
            overwrites = {} if not channels_info[channel_name]['overwrites'] else \
                ChannelParser.__overwrites_parser__(channels_info[channel_name]['overwrites'],
                                                    permissions_groups, roles)

            default_perm = permissions_groups[channels_info[channel_name]['default_perm']].permissions_overwrite

            new_channel = Channel(channel_name_format(channels_info[channel_name]['name']), overwrites, default_perm)
            channels[channel_name] = new_channel

        logger.info('{} channels parsed'.format(len(channels_info)))
        return channels
