from fastapi import APIRouter, HTTPException, status

from repository.connect import LocalSessionDB
from repository.organization import OrganizationRepository
from server.organization import OrganizationServer
from untils.exception.organization import OrganizationNotFound
from schems.organization import GetOrganization


organization = APIRouter(
    prefix='/api/v1',
    tags=['Organization']
)


@organization.get(
    '/{organization_id}',
    response_model=GetOrganization
)
async def get_organization_by_id(
    organization_id: int
):
    try:
        async with LocalSessionDB() as session:
            repo = OrganizationRepository(session=session.session)
            server = OrganizationServer(repository=repo)

            organization_ = await server.get_organization(
                organization_id=organization_id
            )

            return organization_
    except OrganizationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_510_NOT_EXTENDED,
            detail=str(e)
        )


@organization.get(
    '/name/{organization_name}',
    response_model=GetOrganization
)
async def get_organization_by_name(
    organization_name: str
):
    try:
        async with LocalSessionDB() as session:
            repo = OrganizationRepository(session=session.session)
            server = OrganizationServer(repository=repo)

            organization_ = await server.get_organization_by_name(
                organization_name=organization_name
            )

            return organization_
    except OrganizationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_510_NOT_EXTENDED,
            detail=str(e)
        )