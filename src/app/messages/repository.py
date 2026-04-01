from dataclasses import asdict
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import MessageEntity
from .domain import Message, NewMessage


def _to_domain(entity: MessageEntity) -> Message:
    return Message(
        id=entity.id,
        chat_id=entity.chat_id,
        role=entity.role,
        content=entity.content,
        created_at=entity.created_at,
    )


def create_message(db: Session, new_message: NewMessage) -> Message:
    entity = MessageEntity(**asdict(new_message))
    db.add(entity)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def get_message_by_id(db: Session, message_id: UUID) -> Message | None:
    entity = db.get(MessageEntity, message_id)
    return _to_domain(entity) if entity else None


def get_messages_by_chat(db: Session, chat_id: UUID) -> list[Message]:
    entities = db.scalars(
        select(MessageEntity).where(MessageEntity.chat_id == chat_id).order_by(MessageEntity.created_at.asc())
    ).all()
    return [_to_domain(e) for e in entities]


def delete_message(db: Session, message_id: UUID) -> bool:
    entity = db.get(MessageEntity, message_id)
    if not entity:
        return False
    db.delete(entity)
    db.flush()
    return True
