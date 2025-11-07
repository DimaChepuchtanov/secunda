from typing import List, Dict

from repository.model import Incident
from schems.incident import CreateIncident, UpdateIncident
from repository.incedent import IncidentRepository
from untils.exceptions.incident import IncidentNotFound


class IncidentServer:
    def __init__(self, repository):
        self.repository: IncidentRepository = repository

    async def get_incidents(self) -> List[dict]:
        """
        Retrieves all incidents from the repository.

        Returns:
            List[dict]: A list of dictionaries representing all incidents.
        """
        incidents = await self.repository.get_incidents()

        incidents_dict = [incident.dict() for incident in incidents]

        return incidents_dict

    async def get_incident_by_id(self, incident_id: str) -> Dict[str, str]:
        """
        Retrieves a specific incident by its ID.

        Args:
            incident_id (str): The unique identifier of the incident.

        Returns:
            Dict[str, str]: A dictionary representing the incident.

        Raises:
            IncidentNotFound: If the incident is not found.
        """
        incident: Incident = await self.repository.get_incident(
            incident_id=incident_id
        )

        if not incident:
            raise IncidentNotFound(id=incident_id)

        return incident.dict()

    async def get_incidents_by_status(self, status: str) -> List[dict]:
        """
        Retrieves incidents filtered by their status.

        Args:
            status (str): The status to filter incidents by.

        Returns:
            List[dict]: A list of dictionaries representing incidents with the specified status.
        """
        incidents: Incident = await self.repository.get_incident_with_filter(
            filter={"status": status}
        )

        incidents_dict = [incident.dict() for incident in incidents]

        return incidents_dict

    async def create_incident(self, incident_data: CreateIncident) -> Dict[str, str]:
        """
        Creates a new incident with the provided data.

        Args:
            incident_data (CreateIncident): The data for creating the incident.

        Returns:
            Dict[str, str]: A dictionary representing the created incident.
        """
        incident: Incident = await self.repository.create_incident(
            incident_data=incident_data.dict()
        )

        return incident.dict()

    async def update_incident(self, incident_id: str, incident_data: UpdateIncident) -> Dict[str, str]:
        """
        Updates an existing incident with new data.

        Args:
            incident_id (str): The unique identifier of the incident to update.
            incident_data (UpdateIncident): The updated data for the incident.

        Returns:
            Dict[str, str]: A dictionary representing the updated incident.

        Raises:
            IncidentNotFound: If the incident is not found.
        """
        incident: Incident = await self.repository.get_incident(
            incident_id=incident_id
        )

        if not incident:
            raise IncidentNotFound(id=incident_id)

        incident: Incident = await self.repository.update_incident(
            incident_id=incident_id,
            incident_data=incident_data.dict()
        )

        return incident.dict()

    async def delete_incident(self, incident_id: str):
        """
        Deletes an incident by its ID.

        Args:
            incident_id (str): The unique identifier of the incident to delete.

        Raises:
            IncidentNotFound: If the incident is not found.
        """
        incident: Incident = await self.repository.get_incident(
            incident_id=incident_id
        )

        if not incident:
            raise IncidentNotFound(id=incident_id)

        await self.repository.delete_incident(incident_id=incident_id)
