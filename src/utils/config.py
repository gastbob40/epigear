import logging
import os
import re
from typing import Dict

import yaml

from src.models.permission_group import PermissionGroup
from src.yaml_parser.permissions_parser import PermissionGroupParser

# Logger
logger = logging.getLogger("epigear_logger")


class Config:
    prefix: str
    perm_group_path: str
    guilds: Dict[int, Dict[str, PermissionGroup]]

    def __init__(self, config: Dict, perm_group_path: str):
        logger.debug('Build config')

        self.prefix = config["prefix"]
        self.perm_group_path = perm_group_path
        self.guilds = dict()

        for root, dirs, files in os.walk(perm_group_path):
            for file in files:
                pattern = re.compile('[0-9][0-9]*.yml')
                if pattern.match(file):
                    print(file)
                    guild_id: int = int(file.split('.')[0])
                    logger.debug(f'Getting perm group for {guild_id}')

                    self.guilds[guild_id] = PermissionGroupParser.get_permissions(os.path.join(perm_group_path, file))

    def dump_perm_group(self, guild: int):
        """
        Dumps the permission group of the guild
        :param guild: id of the guild
        """
        if guild not in self.guilds.keys():
            return
        name = f"{guild}.yml"
        d = {k: dict(filter(lambda item: item[1] is not None, iter(self.guilds[guild][k].permissions_overwrite))) for
             k in self.guilds[guild]}

        with open(f'{os.path.join(self.perm_group_path, name)}', 'w', encoding="utf8") as stream:
            yaml.safe_dump(d, stream, default_flow_style=False, sort_keys=True, encoding='utf-8',
                           allow_unicode=True)
