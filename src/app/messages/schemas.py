from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class MessageCreate(BaseModel):
    chat_id: UUID
    role: str
    content: str


class MessageResponse(BaseModel):
    id: UUID
    chat_id: UUID
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
