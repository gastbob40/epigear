from argparse import ArgumentParser
import discord
import yaml

from src.events_handler.events_handler import EventsHandler
from src.utils.utils import *
from src.utils.config import Config

# Logger
logger = logging.getLogger("epigear_logger")

with open('run/config_bot/config.yml', 'r', encoding='utf8') as stream:
    config_bot = yaml.safe_load(stream)

client = discord.Client()
config = Config(config_bot, "run/config_servers")


@client.event
async def on_ready():
    logger.info('Epigear has logged in as {0.user}'.format(client))

@client.event
async def on_message(message: discord.Message):
    await EventsHandler.handle_on_message(client, message, config)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help="show debug messages")
    args = parser.parse_args()
    define_logger(args)
    logger.info('Launching EpiGear')
    logger.debug('Debug Mod Enabled')

    client.run(config_bot['token'])
