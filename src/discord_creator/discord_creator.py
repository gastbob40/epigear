from typing import Dict

import discord

from src.models.permission_group import PermissionGroup
from src.models.role import Role
from src.yaml_parser.channels_parser import ChannelParser
from src.yaml_parser.permissions_parser import PermissionGroupParser
from src.yaml_parser.role_parser import RoleParser
from src.yaml_parser.role_promo_parser import RolePromoParser


class DiscordCreator:
    permissions_groups: Dict[str, PermissionGroup]
    roles: Dict[str, Role]
    promo_roles: Dict[str, Role]
    all_roles: Dict[str, Role]
    guild: discord.Guild

    def __init__(self, client: discord.Client, current_promo: int, guild_id: int):
        # Get data from parser
        self.permissions_groups = PermissionGroupParser.yaml_to_objects()
        self.roles = RoleParser.yaml_to_objects(self.permissions_groups)
        self.promo_roles = RolePromoParser.yaml_to_objects(current_promo, self.permissions_groups)
        self.all_roles: Dict[str, Role] = self.roles
        self.guild = client.get_guild(guild_id)
        # all_roles: Dict[str, Role] = {**roles, **promo_roles}

    async def create_role(self):
        for role_name in self.all_roles:
            role = self.all_roles[role_name]
            discord_role = await self.guild.create_role(name=role.name,
                                                        permissions=role.permissions.permissions,
                                                        colour=role.color,
                                                        hoist=role.mentionable,
                                                        mentionable=role.mentionable)

            self.all_roles[role_name].set_role(discord_role)

    async def create_categories_and_channels(self):
        categories = ChannelParser.yaml_to_objects(self.permissions_groups, self.all_roles)
        for category_name in categories:
            category = categories[category_name]
            discord_category = await self.guild.create_category(name=category_name, overwrites=category.overwrites)

            for text_channel_name in category.channels:
                text_channel = category.channels[text_channel_name]
                await self.guild.create_text_channel(name=text_channel.name,
                                                     overwrites=text_channel.overwrites,
                                                     category=discord_category)
