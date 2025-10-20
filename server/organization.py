from typing import Dict, Any

from repository.organization import OrganizationRepository
from repository.model import Organization
from untils.exception.organization import OrganizationNotFound
from schems.organization import (
    GetOrganization, CreateOrganization,
    UpdateOrganization
)


class OrganizationServer:
    def __init__(self, repository):
        self.repository: OrganizationRepository = repository

    async def get_organization(self, organization_id: int) -> Dict[str, str]:
        organization: Organization = await self.repository.get_organizaiton(
            organization_id=organization_id
        )
        if not organization:
            raise OrganizationNotFound(param=organization_id)

        return organization.dict()

    async def get_organization_by_name(self, organization_name: str) -> Dict[str, str]:
        organization: Organization = await self.repository.get_filter_by(
            filter_data={'name': organization_name}
        )
        if not organization:
            raise OrganizationNotFound(param=organization_name)

        return organization.dict()
