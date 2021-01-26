import logging
from typing import Dict, List

import discord

from src.models.permission_group import PermissionGroup
from src.models.role import Role
from src.models.channels import Category
from src.utils.utils import get_content_from_link
from src.yaml_parser.channels_parser import ChannelParser
from src.yaml_parser.role_parser import RoleParser

logger = logging.getLogger("epigear_logger")


class DiscordCreator:
    permissions_groups: Dict[str, PermissionGroup]
    roles: Dict[str, Role]
    all_roles: Dict[str, Role]
    roles_to_ignore: List[int]
    client: discord.Client
    guild: discord.Guild
    guild_id: int

    def __init__(self, client: discord.Client, guild_id: int, permissions_groups: Dict[str, PermissionGroup],
                 roles_to_ignore: List[int]):
        # Get data from parser
        self.permissions_groups = permissions_groups
        self.roles_to_ignore = roles_to_ignore
        self.client = client
        self.guild = client.get_guild(guild_id)
        self.guild_id = guild_id

    async def create_all(self, role_link: str, channels_link: str):
        try:
            roles = get_content_from_link(role_link)
            self.roles = RoleParser.get_roles_from_content(roles, self.permissions_groups)
            self.all_roles: Dict[str, Role] = {**self.roles}
        except Exception as e:
            raise Exception(f"Error during the parsing of the roles from {role_link}: \n{e}")

        try:
            await self.create_role(self.roles_to_ignore)
        except Exception as e:
            raise Exception(f"Error during the creation of the roles from {role_link}: \n{e}")

        try:
            content = get_content_from_link(channels_link)
            channels = ChannelParser.get_channels_from_file(content, self.permissions_groups, self.all_roles)
        except Exception as e:
            raise Exception(f"Error during the parsing of the channels from {channels_link}: \n{e}")

        try:
            await self.create_categories_and_channels(channels)
        except Exception as e:
            raise Exception(f"Error during the creation of the channels from {channels_link}: \n{e}")

    async def create_role(self, roles_to_ignore: List[int]):
        logger.debug("Creating/Updating roles")
        for role_name in self.all_roles:
            role = self.all_roles[role_name]

            if role_name in roles_to_ignore:
                logger.debug("role {}:{} ignored".format(role_name, role.name))
                continue

            logger.debug("creating/updating role {}:{}".format(role_name, role.name))

            discord_role: discord.Role = discord.utils.get(self.guild.roles, name=role.name)

            if discord_role is None:
                discord_role = await self.guild.create_role(name=role.name,
                                                            permissions=role.permissions.permissions,
                                                            colour=role.color,
                                                            hoist=role.hoist,
                                                            mentionable=role.mentionable)
            else:
                await discord_role.edit(name=role.name,
                                        permissions=role.permissions.permissions,
                                        colour=role.color,
                                        hoist=role.hoist,
                                        mentionable=role.mentionable)
            self.all_roles[role_name].set_role(discord_role)
        logger.debug("All roles created/updated")

    async def create_categories_and_channels(self, categories: Dict[str, Category]):

        logger.debug("Creating/Updating categories and channels")

        for category_name in categories:
            category = categories[category_name]
            logger.debug("creating/updating category {}:{}".format(category_name, category.name))

            # Create discord category
            discord_category: discord.CategoryChannel = discord.utils.get(self.guild.categories, name=category.name)
            # Add the default role
            category.overwrites[self.guild.default_role] = category.default_perm
            if discord_category is None:
                discord_category = await self.guild.create_category_channel(name=category.name,
                                                                            overwrites=category.overwrites)
            else:
                for role in category.overwrites:
                    await discord_category.set_permissions(role, overwrite=category.overwrites[role])

            # Create discord channel
            for text_channel_name in category.channels:
                text_channel = category.channels[text_channel_name]
                logger.debug("creating/updating text channel {}:{}".format(text_channel_name, text_channel.name))
                text_channel.overwrites[self.guild.default_role] = text_channel.default_perm
                discord_text_channel: discord.TextChannel = \
                    discord.utils.get(self.guild.text_channels, name=text_channel.name, category_id=discord_category.id)

                if discord_text_channel is None:
                    discord_text_channel = await self.guild.create_text_channel(name=text_channel.name,
                                                                                category=discord_category)
                if len(text_channel.overwrites) == 0:
                    await discord_text_channel.edit(sync_permissions=True, topic=text_channel.topic)
                for role in text_channel.overwrites:
                    await discord_text_channel.set_permissions(role, overwrite=text_channel.overwrites[role])

            for voice_channel_name in category.vocal_channels:
                voice_channel = category.vocal_channels[voice_channel_name]
                logger.debug("creating/updating voice channel {}:{}".format(voice_channel_name, voice_channel.name))
                voice_channel.overwrites[self.guild.default_role] = voice_channel.default_perm
                discord_voice_channel: discord.VoiceChannel = \
                    discord.utils.get(self.guild.voice_channels, name=voice_channel.name,
                                      category_id=discord_category.id)

                if discord_voice_channel is None:
                    discord_voice_channel = await self.guild.create_voice_channel(name=voice_channel.name,
                                                                                  category=discord_category)
                if len(voice_channel.overwrites) == 0:
                    await discord_voice_channel.edit(sync_permissions=True)
                for role in voice_channel.overwrites:
                    await discord_voice_channel.set_permissions(role, overwrite=voice_channel.overwrites[role])
        logger.debug("All categories and channels created/updated")

    async def delete__channels(self, channels_to_ignore: List[str]):
        logger.debug('Deleting channels')
        for channel in self.client.get_guild(self.guild_id).channels:
            if channel.name not in channels_to_ignore:
                await channel.delete()

    async def delete_roles(self, roles_to_ignore: List[str]):
        logger.debug('Deleting roles')
        for role in self.client.get_guild(self.guild_id).roles:
            if role.name not in roles_to_ignore and not role.managed and not role.is_default():
                await role.delete()

    async def get_roles_id(self):
        for role in self.all_roles:
            discord_role: discord.Role = self.all_roles[role].role_discord
            if discord_role is not None:
                print(f'{discord_role.name} : {discord_role.id}')
