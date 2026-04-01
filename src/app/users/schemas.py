from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None


class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
