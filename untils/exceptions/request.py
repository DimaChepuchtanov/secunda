class ManyRequest(Exception):
    def __init__(self): pass

    def __str__(self):
        return "Many requests"


class AccessIsDenied(Exception):
    def __init__(self): pass

    def __str__(self):
        return "Access is prohibited"
