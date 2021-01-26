from typing import Dict
import yaml
import logging

from src.models.permission_group import PermissionGroup

logger = logging.getLogger("epigear_logger")


class PermissionGroupParser:

    @staticmethod
    def get_permissions_from_file(path: str) -> Dict[str, PermissionGroup]:
        logger.debug(f'Get permission groups from config for {path}')
        with open(path, 'r', encoding='utf8') as stream:
            data = yaml.safe_load(stream)

        perm_groups = {}

        for perm_group_name in data:
            perm_group = PermissionGroup(perm_group_name)
            if len(data[perm_group_name]) != 0:
                perm_group.permissions.update(**data[perm_group_name])
                perm_group.permissions_overwrite.update(**data[perm_group_name])
            perm_groups[perm_group_name] = perm_group

        return perm_groups
