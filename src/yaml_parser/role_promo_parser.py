from typing import Dict
import yaml
from src.models.permission_group import PermissionGroup
from src.models.role import Role


class RolePromoParser:

    @staticmethod
    def yaml_to_objects(current_promo: int, permissions_groups: Dict[str, PermissionGroup]):
        with open('config/roles_promo.yml', 'r') as stream:
            data = yaml.safe_load(stream)

        colors = RolePromoParser.__get_colors__(current_promo, data)



        roles = {}

    @staticmethod
    def __get_colors__(current_promo: int, data: any) -> Dict[str, int]:
        colors = {}
        for i in range(current_promo - 4, current_promo + 1):
            colors[f'{i}'] = data['promos'][i]['color']
        return colors

