from typing import Dict,List
import logging
import discord

from src.models.permission_group import PermissionGroup
from src.models.role import Role
from src.yaml_parser.channels_parser import ChannelParser
from src.yaml_parser.permissions_parser import PermissionGroupParser
from src.yaml_parser.role_parser import RoleParser

logger = logging.getLogger()


class DiscordCreator:
    permissions_groups: Dict[str, PermissionGroup]
    roles: Dict[str, Role]
    client: discord.Client
    guild: discord.Guild

    def __init__(self, client: discord.Client, guild_id: int):
        # Get data from parser
        self.permissions_groups = PermissionGroupParser.yaml_to_objects()
        self.roles = RoleParser.yaml_to_objects(self.permissions_groups)
        self.client = client
        self.guild = client.get_guild(guild_id)

    async def create_role(self):
        logger.info('Creating roles in server')
        for role_name in self.roles:
            role = self.roles[role_name]

            discord_role: discord.Role = discord.utils.get(self.guild.roles, name=role.name)

            if discord_role is None:
                discord_role = await self.guild.create_role(name=role.name,
                                                            permissions=role.permissions.permissions,
                                                            colour=role.color,
                                                            hoist=role.mentionable,
                                                            mentionable=role.mentionable)
            else:
                await discord_role.edit(name=role.name,
                                        permissions=role.permissions.permissions,
                                        colour=role.color,
                                        hoist=role.mentionable,
                                        mentionable=role.mentionable)
            self.roles[role_name].set_role(discord_role)

    async def create_categories_and_channels(self):
        logger.info('Creating channels in server')
        categories = ChannelParser.yaml_to_objects(self.permissions_groups, self.roles)
        for category_name in categories:
            category = categories[category_name]

            # Create discord category
            discord_category: discord.CategoryChannel = discord.utils.get(self.guild.categories, name=category.name)
            # Add the default role
            category.overwrites[self.guild.default_role] = category.default_perm
            if discord_category is None:
                discord_category = await self.guild.create_category_channel(name=category.name,
                                                                            overwrites=category.overwrites)
            else:
                await discord_category.edit(overwrites=category.overwrites)

            # Create discord channel
            for text_channel_name in category.channels:
                text_channel = category.channels[text_channel_name]
                text_channel.overwrites[self.guild.default_role] = text_channel.default_perm
                discord_channel: discord.TextChannel = \
                    discord.utils.get(self.guild.text_channels, name=text_channel.name, category_id=discord_category.id)

                if discord_channel is None:
                    discord_channel = await self.guild.create_text_channel(name=text_channel.name,
                                                                           category=discord_category)
                    await discord_channel.edit(sync_permissions=True)
                    for role in text_channel.overwrites:
                        await discord_channel.set_permissions(role, overwrite=text_channel.overwrites[role])

                else:
                    await discord_channel.edit(sync_permissions=True)
                    for role in text_channel.overwrites:
                        await discord_channel.set_permissions(role, overwrite=text_channel.overwrites[role])

            for voice_channel_name in category.vocal_channels:
                voice_channel = category.vocal_channels[voice_channel_name]
                voice_channel.overwrites[self.guild.default_role] = voice_channel.default_perm
                discord_channel: discord.VoiceChannel = \
                    discord.utils.get(self.guild.voice_channels, name=voice_channel.name,
                                      category_id=discord_category.id)

                if discord_channel is None:
                    discord_channel = await self.guild.create_voice_channel(name=voice_channel.name,
                                                                            category=discord_category)
                    await discord_channel.edit(sync_permissions=True)
                    for role in voice_channel.overwrites:
                        await discord_channel.set_permissions(role, overwrite=voice_channel.overwrites[role])

                else:
                    await discord_channel.edit(sync_permissions=True)
                    for role in voice_channel.overwrites:
                        await discord_channel.set_permissions(role, overwrite=voice_channel.overwrites[role])

    async def delete_channels(self, channels_to_ignore: List[str]):
        logger.info('Deleting channels')
        for channel in self.client.get_guild(601889323801116673).channels:
            if channel.name not in channels_to_ignore:
                await channel.delete()
                
    async def delete_roles(self, roles_to_ignore: List[str]):
        logger.info('Deleting roles')
        for role in self.client.get_guild(601889323801116673).roles:
            if role.name not in roles_to_ignore:
                await role.delete()
