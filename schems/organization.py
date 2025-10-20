import re

from pydantic import BaseModel, validator
from fastapi import HTTPException, status


class GetOrganization(BaseModel):
    name: str
    phone: list
    address: str
    # activity: str


class CreateOrganization(BaseModel):
    name: str
    phone: list

    @validator("name")
    def validate_name(value):
        if len(value) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка параметра 'name', длинна должна быть не меньше 3х символов"
            )
        return value

    @validator("phone")
    def validate_phone(value):
        pattern = r'(\+7|7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
        for phone in value:
            if not bool(re.match(pattern, phone)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ошибка параметра 'phone', неверный формат номера"
                )
        return ";".join(value)

    def dict(self):
        return {
            "name": self.name,
            "phone": self.phone
        }


class UpdateOrganization(CreateOrganization):
    pass
