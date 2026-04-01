from dataclasses import asdict
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import ChatEntity
from .domain import Chat, NewChat, ChatChanges


def _to_domain(entity: ChatEntity) -> Chat:
    return Chat(
        id=entity.id,
        user_id=entity.user_id,
        title=entity.title,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def create_chat(db: Session, new_chat: NewChat) -> Chat:
    entity = ChatEntity(user_id=new_chat.user_id, title=new_chat.title)
    db.add(entity)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def get_chat_by_id(db: Session, chat_id: UUID) -> Chat | None:
    entity = db.get(ChatEntity, chat_id)
    return _to_domain(entity) if entity else None


def get_all_chats(db: Session) -> list[Chat]:
    entities = db.scalars(select(ChatEntity).order_by(ChatEntity.created_at.desc())).all()
    return [_to_domain(e) for e in entities]


def get_chats_by_user(db: Session, user_id: UUID) -> list[Chat]:
    entities = db.scalars(
        select(ChatEntity).where(ChatEntity.user_id == user_id).order_by(ChatEntity.created_at.desc())
    ).all()
    return [_to_domain(e) for e in entities]


def update_chat(db: Session, chat_id: UUID, changes: ChatChanges) -> Chat | None:
    entity = db.get(ChatEntity, chat_id)
    if not entity:
        return None
    for key, value in asdict(changes).items():
        if value is not None:
            setattr(entity, key, value)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def delete_chat(db: Session, chat_id: UUID) -> bool:
    entity = db.get(ChatEntity, chat_id)
    if not entity:
        return False
    db.delete(entity)
    db.flush()
    return True
