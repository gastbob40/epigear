class Permission:
    name: str
    value: bool

    def __init__(self, name: str, value: bool):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}: {self.value}"
