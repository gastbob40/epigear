from argparse import ArgumentParser
import discord
import yaml
from src.discord_creator.discord_creator import DiscordCreator
from src.utils import *

# Logger
logger = logging.getLogger(__name__)

with open('run/config_bot/config.default.yml', 'r') as stream:
    config_bot = yaml.safe_load(stream)

client = discord.Client()


@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

    discord_creator = DiscordCreator(client, config_bot['discord_server_id'])

    if config_bot['clear']:
        channels_to_ignore = config_bot['channels_to_ignore'] if not config_bot['channels_to_ignore'] is None else []
        roles_to_ignore = config_bot['roles_to_ignore'] if not config_bot['roles_to_ignore'] is None else []
        await discord_creator.delete_all(channels_to_ignore, roles_to_ignore)

    await discord_creator.create_role()
    await discord_creator.create_categories_and_channels()

    quit()

def main():
    client.run(config_bot['token'])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help="show debug messages")
    args = parser.parse_args()
    define_logger(args)
    logger.info('Launching EpiGear')
    logger.debug('Debug Mod Enabled')

    main()