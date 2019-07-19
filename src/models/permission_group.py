from typing import List
from src.models.permission import Permission


class PermissionGroup:
    name: str
    permissions: List[Permission]

    def __init__(self, name: str):
        self.name = name
        self.permissions = []

    def __str__(self):
        return self.name
