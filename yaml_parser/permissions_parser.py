from typing import List
import yaml
from models.permission import Permission
from models.permission_group import PermissionGroup


class PermissionGroupParser:

    @staticmethod
    def yaml_to_objects() -> List[PermissionGroup]:
        with open('config/perms_groups.yml', 'r') as stream:
            data = yaml.safe_load(stream)
            perms_group = []

            # For all permission group
            for perm_group_name in data:
                perm_group = PermissionGroup(perm_group_name)

                # For all permission in a permission group
                for perm_name in data[perm_group_name]:
                    value = data[perm_group_name][perm_name]
                    perm_group.permissions.append(Permission(perm_name, value))

                perms_group.append(perm_group)

            return perms_group
