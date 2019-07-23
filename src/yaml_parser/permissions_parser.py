from typing import Dict
import yaml
import logging

from src.models.permission_group import PermissionGroup

logger = logging.getLogger()


class PermissionGroupParser:

    @staticmethod
    def yaml_to_objects() -> Dict[str, PermissionGroup]:
        logger.info('Get permission groups from config')
        with open('run/config_server/perms_groups.yml', 'r') as stream:
            data = yaml.safe_load(stream)
        perm_groups = {}

        for perm_group_name in data:
            logger.debug('Parsing perm group {}'.format(perm_group_name))
            perm_group = PermissionGroup(perm_group_name)
            if(len(data[perm_group_name]) != 0):
                perm_group.permissions.update(**data[perm_group_name])
                perm_group.permissions_overwrite.update(**data[perm_group_name])
            perm_groups[perm_group_name] = perm_group

        logger.info('{} permission groups parsed'.format(len(data)))
        return perm_groups

