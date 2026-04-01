from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class ChatCreate(BaseModel):
    user_id: UUID
    title: str | None = None


class ChatUpdate(BaseModel):
    title: str | None = None


class ChatResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
