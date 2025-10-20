from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from repository.model import Organization


class OrganizationRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def __get(self, organization_id: int) -> Optional[Organization]:
        result = await self.session.execute(
            select(Organization).
            where(Organization.id == organization_id).
            options(
                selectinload(Organization.address)
            )
        )
        return result.scalars().first()

    async def get_organizaiton(self, organization_id: int) -> Optional[Organization]:
        return await self.__get(organization_id=organization_id)

    async def get_filter_by(self, filter_data: Dict[str, Any]) -> Optional[Organization]:
        result = await self.session.execute(
            select(Organization).
            filter_by(**filter_data).
            options(
                selectinload(Organization.address)
            )
        )
        return result.scalars().first()

    async def create_organization(self, organization_data: Dict[str, Any]) -> Organization:
        organization = Organization()

        for key, value in organization_data.items():
            if hasattr(organization, key):
                setattr(organization, key, value)

        self.session.add(organization)

        return organization

    async def update_organization(
        self,
        organization_id: int,
        organization_data: Dict[str, Any]
    ) -> Organization:
        organization: Organization = await self.__get(
            organization_id=organization_id
        )

        for key, value in organization_data.items():
            if hasattr(organization, key):
                setattr(organization, key, value)

        await self.session.flush(organization)

        return organization

    async def delete_organization(self, organization_id: int):
        organization: Organization = await self.__get(
            organization_id=organization_id
        )

        await self.session.delete(organization)
