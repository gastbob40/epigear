from src.yaml_parser.permissions_parser import PermissionGroupParser
from src.yaml_parser.role_promo_parser import RolePromoParser


permission_groups = PermissionGroupParser.yaml_to_objects()
role_promo = RolePromoParser.yaml_to_objects(2024, permission_groups)


