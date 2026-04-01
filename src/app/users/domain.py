from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class User:
    id: UUID
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    updated_at: datetime


@dataclass
class NewUser:
    first_name: str
    last_name: str
    email: str


@dataclass
class UserChanges:
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
