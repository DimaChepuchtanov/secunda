class OrganizationNotFound(Exception):
    def __init__(self, param):
        self.param = param

    def __str__(self):
        return f"Организация со значением '{self.param}' не найдена"
