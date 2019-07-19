from typing import Dict

import discord
import yaml

from src.models.role import Role
from src.yaml_parser.permissions_parser import PermissionGroupParser
from src.yaml_parser.role_parser import RoleParser
from src.yaml_parser.role_promo_parser import RolePromoParser
from src.yaml_parser.channels_parser import ChannelParser

with open('run/config_bot/config.yml', 'r') as stream:
    config_bot = yaml.safe_load(stream)

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    permissions_groups = PermissionGroupParser.yaml_to_objects()
    roles = RoleParser.yaml_to_objects(permissions_groups)
    promo_roles = RolePromoParser.yaml_to_objects(2024, permissions_groups)
    all_roles: Dict[str, Role] = roles
    #all_roles: Dict[str, Role] = {**roles, **promo_roles}

    guild = client.get_guild(config_bot['discord_server_id'])
    print(f'Creating the server : {guild.id}')

    for role_name in all_roles:
        role = all_roles[role_name]
        discord_role = await guild.create_role(name=role.name,
                                               permissions=role.permissions.permissions,
                                               colour=role.color,
                                               hoist=role.mentionable,
                                               mentionable=role.mentionable)

        all_roles[role_name].set_role(discord_role)

    categories = ChannelParser.yaml_to_objects(permissions_groups, all_roles)

    for category_name in categories:
        category = categories[category_name]
        discord_category = await guild.create_category(name=category_name, overwrites=category.overwrites)

        for text_channel_name in category.channels:
            text_channel = category.channels[text_channel_name]
            await guild.create_text_channel(name=text_channel.name,
                                            overwrites=text_channel.overwrites,
                                            category=discord_category)

client.run(config_bot['token'])