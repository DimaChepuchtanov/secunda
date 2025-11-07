from pydantic import BaseModel, validator
from fastapi import HTTPException, status


class GetIncident(BaseModel):
    id: str
    text: str
    status: str
    author: str
    created_at: str


class CreateIncident(BaseModel):
    text: str
    author: str

    @validator("text")
    def validate_text(value):
        if len(value) < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid text. Need len more then 1"
            )
        return value

    @validator("author")
    def validate_author(value):
        if value not in ["operator", "monitoring", "partner"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid author. Check documentation"
            )
        return value

    def dict(self):
        return {
            "text": self.text,
            "author": self.author
        }


class UpdateIncident(CreateIncident):
    status: str

    @validator("status")
    def validate_status(value):
        if value not in ["created", "checked", "in work", "closed"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status. Check documentation"
            )
        return value

    def dict(self):
        return {
            "text": self.text,
            "author": self.author,
            "status": self.status
        }
