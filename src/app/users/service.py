from uuid import UUID
from sqlalchemy.orm import Session
from . import repository
from .domain import User, NewUser, UserChanges
from ..exceptions import UserNotFoundError


def create_user(db: Session, new_user: NewUser) -> User:
    return repository.create_user(db, new_user)


def get_user(db: Session, user_id: UUID) -> User:
    user = repository.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user


def list_users(db: Session) -> list[User]:
    return repository.get_all_users(db)


def update_user(db: Session, user_id: UUID, changes: UserChanges) -> User:
    user = repository.update_user(db, user_id, changes)
    if not user:
        raise UserNotFoundError(user_id)
    return user


def delete_user(db: Session, user_id: UUID) -> None:
    if not repository.delete_user(db, user_id):
        raise UserNotFoundError(user_id)
