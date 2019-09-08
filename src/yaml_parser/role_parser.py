from typing import Dict
import yaml
import logging

from src.models.role import Role
from src.models.permission_group import PermissionGroup

logger = logging.getLogger()


class RoleParser:

    @staticmethod
    def yaml_to_objects(permissions_groups: Dict[str, PermissionGroup]) -> Dict[str, Role]:
        logger.info('Get roles from config')
        with open('run/config_server/roles.yml', 'r', encoding='utf8') as stream:
            data = yaml.safe_load(stream)

        roles = {}

        for role_name in data:
            logger.debug('Parsing role {}'.format(role_name))
            new_role = Role(data[role_name]['name'], data[role_name]['color'],
                            permissions_groups[data[role_name]['permissions']], data[role_name]['hoist'],
                            data[role_name]['mentionable'])
            roles[role_name] = new_role

        logger.info('{} roles parsed'.format(len(data)))
        return roles
