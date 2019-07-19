from models.permission import Permission


class Role:
    name: str
    color: str
    permissions: Permission
    hoist: bool
    mentionable: bool

    def __init__(self, name: str, color: str = None, permissions: Permissions = None,
                 hoist: bool = False, mentionable: bool = False):
        self.name = name
        self.color = color
        self.permissions = permissions
        self.hoist = hoist
        self.mentionable = mentionable

