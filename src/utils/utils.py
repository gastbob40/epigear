import logging
import sys
import discord
from typing import Dict

from src.models.permission_group import PermissionGroup

logger = logging.getLogger("epigear_logger")


def define_logger(args):
    logging.getLogger("discord").setLevel(logging.WARNING)
    log_format = '%(asctime)s - %(levelname)-7s - %(name)15s:%(lineno)3s - %(funcName)-15s - %(message)s'
    level = logging.INFO if not args.debug else logging.DEBUG
    logger.setLevel(level)

    f = logging.Formatter(log_format)

    handler_stdout = logging.StreamHandler(stream=sys.stdout)
    handler_stdout.setLevel(level)
    handler_stdout.addFilter(lambda record: record.levelno <= logging.INFO)
    handler_stdout.setFormatter(f)
    logger.addHandler(handler_stdout)

    handler_stderr = logging.StreamHandler()
    handler_stderr.setLevel(logging.WARNING)
    handler_stderr.setFormatter(f)
    logger.addHandler(handler_stderr)


def channel_name_format(name: str):
    return str.lower(name).replace(' ', '-')


def category_name_format(name: str):
    return str.upper(name)


def str_to_bool(v: str) -> bool:
    s = v.lower()
    return True if s == 'true' else False if s == 'false' else None


def get_perm_group(d: Dict[str, PermissionGroup], perm: discord.Permissions) -> str:
    for k, v in d.items():
        if v.permissions == perm:
            return k
    return "UNKNOWN"


def get_perm_overwrite_group(d: Dict[str, PermissionGroup], perm: discord.PermissionOverwrite) -> str:
    for k, v in d.items():
        if v.permissions_overwrite == perm:
            return k
    return "UNKNOWN"
