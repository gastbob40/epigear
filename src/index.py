from src.yaml_parser.permissions_parser import PermissionGroupParser
from src.yaml_parser.role_parser import RoleParser

permissions_groups = PermissionGroupParser.yaml_to_objects()

roles = RoleParser.yaml_to_objects(permissions_groups)

for key in roles:
    print('role : {} defined by {}'.format(key, str(roles[key])))



