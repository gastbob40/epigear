from src.yaml_parser.permissions_parser import PermissionGroupParser
from src.yaml_parser.role_parser import RoleParser
from src.yaml_parser.role_promo_parser import RolePromoParser

permissions_groups = PermissionGroupParser.yaml_to_objects()
roles = RoleParser.yaml_to_objects(permissions_groups)
promo_roles = RolePromoParser.yaml_to_objects(2024, permissions_groups)

