import logging
from typing import Dict

import yaml
from discord import PermissionOverwrite
from discord import Role as RoleDiscord

from src.models.channels import Channel, Category
from src.models.permission_group import PermissionGroup
from src.models.role import Role
from src.utils.utils import channel_name_format

logger = logging.getLogger("epigear_logger")


class ChannelParser:

    @staticmethod
    def get_channels_from_file(content: str, permissions_groups: Dict[str, PermissionGroup],
                               roles: Dict[str, Role]) -> Dict[str, Category]:
        data = yaml.safe_load(content)
        logger.debug('Get categories from config')

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

        logger.debug('{} categories parsed'.format(len(data)))

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

            topic = "" if "topic" not in channels_info[channel_name] else channels_info[channel_name]["topic"]

            new_channel = Channel(channel_name_format(channels_info[channel_name]['name']),
                                  overwrites,
                                  default_perm,
                                  topic)
            channels[channel_name] = new_channel

        logger.debug('{} channels parsed'.format(len(channels_info)))
        return channels
