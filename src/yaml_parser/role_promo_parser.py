from typing import Dict
import yaml
from src.models.permission_group import PermissionGroup
from src.models.role import Role


class RolePromoParser:

    @staticmethod
    def yaml_to_objects(current_promo: int, permissions_groups: Dict[str, PermissionGroup]):
        with open('run/config_server/roles_promo.yml', 'r') as stream:
            data = yaml.safe_load(stream)

        colors = RolePromoParser.__get_colors__(current_promo, data)
        roles = {}
        current_promo += 1

        for role_name in data['roles_template']:
            new_role = Role(str(current_promo), colors[str(current_promo)],
                            permissions_groups[data['roles_template'][role_name]['permissions']],
                            data['roles_template'][role_name]['hoist'],
                            data['roles_template'][role_name]['mentionable'])

            roles[role_name] = new_role
            current_promo -= 1

        return roles

    @staticmethod
    def __get_colors__(current_promo: int, data: any) -> Dict[str, int]:
        colors = {}
        for i in range(current_promo - 4, current_promo + 2):
            try:
                colors[f'{i}'] = data['promos'][i]['color']
            except:
                colors[f'{i}'] = 0xffffff
        return colors

