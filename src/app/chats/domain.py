from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Chat:
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    title: str | None = None


@dataclass
class NewChat:
    user_id: UUID
    title: str | None = None


@dataclass
class ChatChanges:
    title: str | None = None
