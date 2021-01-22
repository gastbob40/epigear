import fnmatch
import logging
import os
from typing import Dict

from src.models.permission_group import PermissionGroup
from src.yaml_parser.permissions_parser import PermissionGroupParser


# Logger
logger = logging.getLogger("epigear_logger")


class Config:

    prefix: str
    guilds: Dict[int, Dict[str, PermissionGroup]]

    def __init__(self, config : Dict, perm_group_path: str):

        logger.debug('Build config')

        self.prefix = config["prefix"]
        self.guilds = {}

        for root, dirs, files in os.walk(perm_group_path):
            for file in files:
                if fnmatch.fnmatch(file, '[0-9][0-9]*.yml'):

                    guild_id: int = int(file.split('.')[0])
                    logger.debug(f'Getting perm group for {guild_id}')

                    self.guilds[guild_id] = PermissionGroupParser.get_permissions(os.path.join(perm_group_path, file))
