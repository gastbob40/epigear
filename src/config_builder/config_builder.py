import logging
from typing import Dict, List
import yaml

import discord

from src.models.permission_group import PermissionGroup
from src.yaml_parser.permissions_parser import PermissionGroupParser

logger = logging.getLogger()


class ConfigBuilder:
    permissions_groups: Dict[str, PermissionGroup]
    guild: discord.guild
    client: discord.client

    def __init__(self, client: discord.Client, guild_id: int):
        # Get data from parser
        self.permissions_groups = PermissionGroupParser.yaml_to_objects()
        self.client = client
        self.guild = client.get_guild(guild_id)

    def get_perm_group(self, perm: discord.Permissions) -> str:
        for k, v in self.permissions_groups.items():
            if v.permissions == perm:
                return k
        return "UNKNOWN"

    def get_perm_overwrite_group(self, perm: discord.PermissionOverwrite) -> str:
        for k, v in self.permissions_groups.items():
            if v.permissions_overwrite == perm:
                return k
        return "UNKNOWN"

    @staticmethod
    def normalize_name(name: str) -> str:
        for old, new in zip(['(', ')', 'é', 'à', 'è', 'ê', 'ô', 'û', '-', ' '],
                            ['', '', 'e', 'a', 'e', 'e', 'o', 'u', '_', '_']):
            name = name.replace(old, new)
        return name.upper()

    def create_config(self):
        logger.info("Creating config files for server {}".format(self.guild.name))
        roles = {}
        for role in reversed(self.guild.roles):
            if role.name == '@everyone':
                continue
            roles[ConfigBuilder.normalize_name(role.name)] = {"name": role.name,
                                                              "color": "0x" + str(role.color)[1:],
                                                              "permissions": self.get_perm_group(role.permissions),
                                                              "hoist": role.hoist,
                                                              "mentionable": role.mentionable}
        with open(r'run/config_server/roles_{}.yml'.format(self.guild.name), 'w', encoding="utf8") as stream:
            yaml.safe_dump(roles, stream, default_flow_style=False, sort_keys=False, encoding='utf-8',
                           allow_unicode=True)
        categories: Dict = {}
        for cat in self.guild.categories:
            text_channels = {}
            voice_channels = {}

            for chan in cat.text_channels:
                overwrites = {}
                if not chan.permissions_synced:
                    for role, overwrite in chan.overwrites.items():
                        if type(role) != discord.Role or role.name == "@everyone":
                            continue
                        overwrites[ConfigBuilder.normalize_name(role.name)] = self.get_perm_overwrite_group(overwrite)
                default = self.get_perm_overwrite_group(chan.overwrites_for(self.guild.default_role))
                text_channels[ConfigBuilder.normalize_name(chan.name)] = {"name": chan.name,
                                                                          "overwrites": overwrites.copy(),
                                                                          "default_perm": default}
            for chan in cat.voice_channels:
                overwrites = {}
                if not chan.permissions_synced:
                    for role, overwrite in chan.overwrites.items():
                        if type(role) != discord.Role or role.name == "@everyone":
                            continue
                        overwrites[ConfigBuilder.normalize_name(role.name)] = self.get_perm_overwrite_group(overwrite)
                default = self.get_perm_overwrite_group(chan.overwrites_for(self.guild.default_role))
                voice_channels[ConfigBuilder.normalize_name(chan.name)] = {"name": chan.name,
                                                                           "overwrites": overwrites.copy(),
                                                                           "default_perm": default}
            overwrites = {}
            for role, overwrite in cat.overwrites.items():
                if type(role) != discord.Role or role.name == "@everyone":
                    continue
                overwrites[ConfigBuilder.normalize_name(role.name)] = self.get_perm_overwrite_group(overwrite)
            default = self.get_perm_overwrite_group(cat.overwrites_for(self.guild.default_role))
            categories[ConfigBuilder.normalize_name(cat.name)] = {"name": cat.name,
                                                                  "overwrites": overwrites.copy(),
                                                                  "default_perm": default,
                                                                  "channels": text_channels,
                                                                  "vocal_channels": voice_channels}

        with open(r'run/config_server/server_channels_{}.yml'.format(self.guild.name), 'w', encoding="utf8") as stream:
            yaml.safe_dump(categories, stream, default_flow_style=False, sort_keys=False, encoding='utf-8',
                           allow_unicode=True)