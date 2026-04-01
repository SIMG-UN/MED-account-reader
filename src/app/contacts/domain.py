from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Contact:
    id: UUID
    user_id: UUID
    name: str
    email: str | None
    phone: str | None
    created_at: datetime
    updated_at: datetime


@dataclass
class NewContact:
    user_id: UUID
    name: str
    email: str | None = None
    phone: str | None = None


@dataclass
class ContactChanges:
    name: str | None = None
    email: str | None = None
    phone: str | None = None
