class IncidentNotFound(Exception):
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return f"Incident with id {self.id} not found"
