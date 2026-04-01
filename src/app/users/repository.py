from dataclasses import asdict
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import UserEntity
from .domain import User, NewUser, UserChanges


def _to_domain(entity: UserEntity) -> User:
    return User(
        id=entity.id,
        first_name=entity.first_name,
        last_name=entity.last_name,
        email=entity.email,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def create_user(db: Session, new_user: NewUser) -> User:
    entity = UserEntity(first_name=new_user.first_name, last_name=new_user.last_name, email=new_user.email)
    db.add(entity)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    entity = db.get(UserEntity, user_id)
    return _to_domain(entity) if entity else None


def get_all_users(db: Session) -> list[User]:
    entities = db.scalars(select(UserEntity).order_by(UserEntity.created_at.desc())).all()
    return [_to_domain(e) for e in entities]


def update_user(db: Session, user_id: UUID, changes: UserChanges) -> User | None:
    entity = db.get(UserEntity, user_id)
    if not entity:
        return None
    for key, value in asdict(changes).items():
        if value is not None:
            setattr(entity, key, value)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def delete_user(db: Session, user_id: UUID) -> bool:
    entity = db.get(UserEntity, user_id)
    if not entity:
        return False
    db.delete(entity)
    db.flush()
    return True
