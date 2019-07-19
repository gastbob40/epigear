from typing import Dict
import yaml
from src.models.permission_group import PermissionGroup


class PermissionGroupParser:

    @staticmethod
    def yaml_to_objects() -> Dict[str, PermissionGroup]:
        with open('config/perms_groups.yml', 'r') as stream:
            data = yaml.safe_load(stream)
        perm_groups = {}

        for perm_group_name in data:
            perm_group = PermissionGroup(perm_group_name)
            perm_group.permissions.update(**data[perm_group_name])
            perm_group.permissions_overwrite.update(**data[perm_group_name])
            perm_groups[perm_group_name] = perm_group

        return perm_groups

