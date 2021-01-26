from typing import Dict
import yaml
import logging

from src.models.role import Role
from src.models.permission_group import PermissionGroup

logger = logging.getLogger("epigear_logger")


class RoleParser:

    @staticmethod
    def get_roles_from_content(content: str, permissions_groups: Dict[str, PermissionGroup]) -> Dict[str, Role]:
        logger.debug('Get roles from config')
        data = yaml.safe_load(content)

        roles = {}

        for role_name in data:
            logger.debug('Parsing role {}'.format(role_name))
            new_role = Role(data[role_name]['name'], int(data[role_name]['color'], 16),
                            permissions_groups[data[role_name]['permissions']], data[role_name]['hoist'],
                            data[role_name]['mentionable'])
            roles[role_name] = new_role

        logger.debug('{} roles parsed'.format(len(data)))
        return roles
