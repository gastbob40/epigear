from src.models.role import Role
from src.models.permission_group import PermissionGroup
from typing import Dict
import yaml


class RoleParser:

    @staticmethod
    def yaml_to_objects(permissions_groups: Dict[str, PermissionGroup]) -> Dict[str, Role]:
        with open('config/roles.yml', 'r') as stream:
            data = yaml.safe_load(stream)

        roles = {}

        for role_name in data:
            new_role = Role(data[role_name]['name'], data[role_name]['color'],
                            permissions_groups[data[role_name]['permissions']], data[role_name]['hoist'],
                            data[role_name]['mentionable'])
            roles[role_name] = new_role

        return roles
