import logging
import sys


def define_logger(args):
    log_format = '%(asctime)s - %(levelname)-7s - %(name)15s:%(lineno)3s - %(funcName)-15s - %(message)s'
    level = logging.INFO if not args.debug else logging.DEBUG
    logging.basicConfig(level=level, stream=sys.stdout, format=log_format)
    logging.captureWarnings(True)


def channel_name_format(name: str):
    return str.lower(name).replace(' ', '-')


def category_name_format(name: str):
    return str.upper(name)
