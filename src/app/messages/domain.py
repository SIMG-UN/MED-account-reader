from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Message:
    id: UUID
    chat_id: UUID
    role: str
    content: str
    created_at: datetime


@dataclass
class NewMessage:
    chat_id: UUID
    role: str
    content: str
