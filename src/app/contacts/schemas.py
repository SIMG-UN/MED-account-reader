from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr | None = None
    phone: str | None = None


class ContactUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class ContactResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    email: str | None
    phone: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
