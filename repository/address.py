from typing import Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from repository.model import Address


class AddressRepository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def __get(self, address_id: int) -> Optional[Address]:
        result = await self.session.execute(
            select(Address).
            where(Address.id == address_id)
        )
        return result.scalars().first()

    async def get_address_filter_by(
        self,
        filter_data: Dict[str, Any]
    ) -> Optional[Address]:
        """Получение адресов с фильтром

        Args:
            session (AsyncSession): _description_
            filter_data (Dict[str, Any]): Фильтры, см. примеры

        Returns:
            Optional[Address]: _description_

        Example:
            filter_data:
                {
                    "city": "Москва",
                    "street": "Ленина",
                    "house_number": 1
                }
        """
        result = await self.session.execute(
            select(Address).
            filter_by(**filter_data)
        )

        return result.scalars().all()

    async def create_address(
        self,
        address_data: Dict[str, Any]
    ) -> Address:
        address = Address()

        for key, value in address_data.items():
            if hasattr(address, key):
                setattr(address, key, value)

        self.session.add(address)
        return address

    async def update_address(
        self,
        address_id: int,
        address_data: Dict[str, Any]
    ) -> Address:
        address: Address = await self.__get(
            address_id=address_id
        )

        for key, value in address_data.items():
            if hasattr(address, key):
                setattr(address, key, value)

        await self.session.flush(address)
        return address

    async def delete_address(
        self,
        address_id: int
    ):
        address: Address = await self.__get(
            address_id=address_id
        )
        await self.session.delete(address)
