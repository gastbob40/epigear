from argparse import ArgumentParser
import discord
import yaml
from src.discord_creator.discord_creator import DiscordCreator
from src.config_builder.config_builder import ConfigBuilder
from src.utils import *

# Logger
logger = logging.getLogger("epigear_logger")

with open('run/config_bot/config.yml', 'r', encoding='utf8') as stream:
    config_bot = yaml.safe_load(stream)

client = discord.Client()
mode = "build"


async def create():
    discord_creator = DiscordCreator(client, config_bot['discord_server_id'])
    roles_to_ignore = config_bot['roles_to_ignore'] if config_bot['roles_to_ignore'] is not None else []

    if config_bot['clear_channels']:
        channels_to_ignore = config_bot['channels_to_ignore'] if config_bot['channels_to_ignore'] is not None else []
        await discord_creator.delete__channels(channels_to_ignore)
    if config_bot['clear_roles']:
        await discord_creator.delete_roles(roles_to_ignore)

    await discord_creator.create_role(roles_to_ignore)
    await discord_creator.create_categories_and_channels()
    await discord_creator.get_roles_id()


async def build():
    config_builder = ConfigBuilder(client, config_bot['discord_server_id'])
    config_builder.create_config()


@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))
    if mode == 'create':
        await create()
    elif mode == 'build':
        await build()
    await client.logout()


def main():
    client.run(config_bot['token'])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help="show debug messages")
    parser.add_argument('-m', '--mode', default='create',
                        help="show debug messages")
    args = parser.parse_args()
    define_logger(args)
    logger.info('Launching EpiGear')
    logger.debug('Debug Mod Enabled')
    mode = args.mode
    main()