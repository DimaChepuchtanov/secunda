from typing import Optional, Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import uuid4

from repository.model import Incident
from untils.exceptions.incident import IncidentNotFound


class IncidentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __get(self, inciden_id: str) -> Optional[Incident]:
        """
        Retrieves an incident by its ID from the database.

        Args:
            inciden_id (str): The unique identifier of the incident.

        Returns:
            Optional[Incident]: The incident object if found, otherwise None.
        """
        result = await self.session.execute(
            select(Incident).
            where(Incident.id == inciden_id)
        )

        return result.scalars().first()

    async def get_incident(self, incident_id: str) -> Optional[Incident]:
        """
        Retrieves an incident by its ID.

        Args:
            incident_id (str): The unique identifier of the incident.

        Returns:
            Optional[Incident]: The incident object if found, otherwise None.
        """
        return await self.__get(inciden_id=incident_id)

    async def get_incident_with_filter(self, filter: Dict[str, Any]) -> Optional[Incident]:
        """
        Retrieves incidents based on the provided filter criteria.

        Args:
            filter (Dict[str, Any]): A dictionary of filter criteria where keys are attribute names of the Incident model.

        Returns:
            List[Incident]: A list of incident objects that match the filter criteria.
        """
        has_attr = {}

        for key, value in filter.items():
            if hasattr(Incident, key):
                has_attr[key] = value

        result = await self.session.execute(
            select(Incident).
            filter_by(**has_attr)
        )

        return result.scalars().all()

    async def get_incidents(self) -> List[Incident]:
        """
        Retrieves all incidents from the database.

        Returns:
            List[Incident]: A list of all incident objects.
        """
        result = await self.session.execute(
            select(Incident)
        )
        return result.scalars().all()

    async def create_incident(self, incident_data: Dict[str, Any]) -> Incident:
        """
        Creates a new incident with the provided data.

        Args:
            incident_data (Dict[str, Any]): A dictionary containing the data for the new incident.

        Returns:
            Incident: The newly created incident object.
        """
        new_incident = Incident(id=str(uuid4()))

        for key, value in incident_data.items():
            if hasattr(new_incident, key):
                setattr(new_incident, key, value)

        self.session.add(new_incident)

        return new_incident

    async def update_incident(self, incident_id: str, incident_data: Dict[str, Any]) -> Incident:
        """
        Updates an existing incident with the provided data.

        Args:
            incident_id (str): The unique identifier of the incident to update.
            incident_data (Dict[str, Any]): A dictionary containing the updated data for the incident.

        Returns:
            Incident: The updated incident object.

        Raises:
            IncidentNotFound: If the incident with the given ID is not found.
        """
        incident = await self.__get(inciden_id=incident_id)

        if not incident:
            raise IncidentNotFound(id=incident_id)

        for key, value in incident_data.items():
            if hasattr(incident, key):
                setattr(incident, key, value)

        return incident

    async def delete_incident(self, incident_id: str):
        """
        Deletes an incident by its ID.

        Args:
            incident_id (str): The unique identifier of the incident to delete.

        Raises:
            IncidentNotFound: If the incident with the given ID is not found.
        """
        incident = await self.__get(inciden_id=incident_id)

        if not incident:
            raise IncidentNotFound(id=incident_id)

        await self.session.delete(incident)
