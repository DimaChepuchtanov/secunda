from fastapi import APIRouter, status as http_code, HTTPException

from repository.incedent import IncidentRepository
from server.incident import IncidentServer
from repository.session import LocalSessionPG
from schems.incident import GetIncident, UpdateIncident, CreateIncident
from untils.exceptions.incident import IncidentNotFound


incident = APIRouter(
    prefix='/incident'
)


@incident.get(
    "/",
    status_code=http_code.HTTP_200_OK
)
async def get_incidents():
    """
    Retrieve all incidents.

    This endpoint fetches all incidents from the database and returns them as a list of dictionaries.
    It is useful for getting an overview of all existing incidents in the system.

    Returns:
        List[dict]: A list of dictionaries, each representing an incident with its details.

    Raises:
        HTTPException: If an unexpected error occurs during the database operation, an HTTP 510 Not Extended error is raised with the error details.
    """
    try:
        async with LocalSessionPG() as engine:
            session = engine.session

            repository = IncidentRepository(session=session)
            server = IncidentServer(repository=repository)

            incidents = await server.get_incidents()

            return incidents
    except Exception as e:
        raise HTTPException(
            status_code=http_code.HTTP_510_NOT_EXTENDED,
            detail=str(e)
        )


@incident.get(
    "/status={status}",
    status_code=http_code.HTTP_200_OK
)
async def get_incidents_by_status(
    status: str
):
    """
    Retrieve incidents filtered by a specific status.

    This endpoint allows filtering incidents based on their current status (e.g., 'open', 'closed').
    It returns a list of incidents that match the provided status.

    Args:
        status (str): The status value to filter incidents by. Must be a valid status string.

    Returns:
        List[dict]: A list of dictionaries representing incidents that have the specified status.

    Raises:
        HTTPException: If an unexpected error occurs during the database operation, an HTTP 510 Not Extended error is raised with the error details.
    """
    try:
        async with LocalSessionPG() as engine:
            session = engine.session

            repository = IncidentRepository(session=session)
            server = IncidentServer(repository=repository)

            incidents = await server.get_incidents_by_status(
                status=status
            )

            return incidents
    except Exception as e:
        raise HTTPException(
            status_code=510,
            detail=str(e)
        )


@incident.get(
    "/{incident_id}",
    response_model=GetIncident,
    status_code=http_code.HTTP_200_OK
)
async def get_incident_by_id(
    incident_id: str
):
    """
    Retrieve a specific incident by its unique ID.

    This endpoint fetches the details of a single incident identified by its ID.
    If the incident does not exist, a 404 error is returned.

    Args:
        incident_id (str): The unique identifier (UUID) of the incident to retrieve.

    Returns:
        GetIncident: A model representing the incident's data, including all relevant fields.

    Raises:
        HTTPException: 
            - 404 Not Found: If the incident with the given ID does not exist.
            - 510 Not Extended: For any other unexpected errors during the operation.
    """
    try:
        async with LocalSessionPG() as engine:
            session = engine.session

            repository = IncidentRepository(session=session)
            server = IncidentServer(repository=repository)

            incident_ = await server.get_incident_by_id(
                incident_id=incident_id
            )

            return incident_
    except IncidentNotFound as e:
        raise HTTPException(
            status_code=http_code.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_code.HTTP_510_NOT_EXTENDED,
            detail=str(e)
        )


@incident.post(
    "/",
    response_model=GetIncident,
    status_code=http_code.HTTP_201_CREATED
)
async def create_incident(
    incident_data: CreateIncident
):
    """
    Create a new incident.

    This endpoint allows the creation of a new incident by providing the necessary data.
    The incident is assigned a unique ID and stored in the database.

    Args:
        incident_data (CreateIncident): A model containing the data for the new incident, such as title, description, status, etc.

    Returns:
        GetIncident: A model representing the newly created incident with its assigned ID and data.

    Raises:
        HTTPException: If an unexpected error occurs during creation, an HTTP 510 Not Extended error is raised with the error details.
    """
    try:
        async with LocalSessionPG() as engine:
            session = engine.session

            repository = IncidentRepository(session=session)
            server = IncidentServer(repository=repository)

            incident_ = await server.create_incident(
                incident_data=incident_data
            )

            return incident_
    except Exception as e:
        raise HTTPException(
            status_code=http_code.HTTP_510_NOT_EXTENDED,
            detail=str(e)
        )


@incident.patch(
    "/{incident_id}",
    response_model=GetIncident,
    status_code=http_code.HTTP_200_OK
)
async def update_incident(
    incident_id: str,
    incident_data: UpdateIncident
):
    """
    Update an existing incident.

    This endpoint updates the details of an incident identified by its ID with the provided data.
    Only the fields included in the update data will be modified.

    Args:
        incident_id (str): The unique identifier (UUID) of the incident to update.
        incident_data (UpdateIncident): A model containing the fields to update, such as status or description.

    Returns:
        GetIncident: A model representing the updated incident with the new data.

    Raises:
        HTTPException: 
            - 404 Not Found: If the incident with the given ID does not exist.
            - 510 Not Extended: For any other unexpected errors during the update.
    """
    try:
        async with LocalSessionPG() as engine:
            session = engine.session

            repository = IncidentRepository(session=session)
            server = IncidentServer(repository=repository)

            incident_ = await server.update_incident(
                incident_id=incident_id,
                incident_data=incident_data
            )

            return incident_
    except IncidentNotFound as e:
        raise HTTPException(
            status_code=http_code.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_code.HTTP_510_NOT_EXTENDED,
            detail=str(e)
        )


@incident.delete(
    "/{incident_id}",
    status_code=http_code.HTTP_204_NO_CONTENT
)
async def delete_incident(
    incident_id: str
):
    """
    Delete an incident by its ID.

    This endpoint permanently removes the incident with the specified ID from the database.
    If the incident does not exist, a 404 error is returned.

    Args:
        incident_id (str): The unique identifier (UUID) of the incident to delete.

    Raises:
        HTTPException: 
            - 404 Not Found: If the incident with the given ID does not exist.
            - 510 Not Extended: For any other unexpected errors during deletion.
    """
    try:
        async with LocalSessionPG() as engine:
            session = engine.session

            repository = IncidentRepository(session=session)
            server = IncidentServer(repository=repository)

            await server.delete_incident(
                incident_id=incident_id
            )
    except IncidentNotFound as e:
        raise HTTPException(
            status_code=http_code.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_code.HTTP_510_NOT_EXTENDED,
            detail=str(e)
        )
