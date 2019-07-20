from argparse import ArgumentParser
import discord
import yaml
from src.discord_creator.discord_creator import DiscordCreator
from src.utils import *

# Logger
logger = logging.getLogger(__name__)

with open('run/config_bot/config.yml', 'r') as stream:
    config_bot = yaml.safe_load(stream)

client = discord.Client()


@client.event
async def on_ready():
    logger.info('We have logged in as {0.user}'.format(client))

    discord_creator = DiscordCreator(client, config_bot['current_promo'], config_bot['discord_server_id'])
    await discord_creator.create_role()
    await discord_creator.create_categories_and_channels()

    # await delete_all()


def main():
    client.run(config_bot['token'])


async def delete_all():
    validation = input("Are you sure you want to delete ? (Y/N)")
    if validation != 'Y':
        return
    for channel in client.get_guild(601889323801116673).channels:
        await channel.delete()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help="show debug messages")
    args = parser.parse_args()
    define_logger(args)
    logger.info('Launching EpiGear')
    logger.debug('Debug Mod Enabled')

    main()
