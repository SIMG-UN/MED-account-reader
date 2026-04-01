from uuid import UUID
from sqlalchemy.orm import Session
from . import repository
from .domain import Message, NewMessage
from ..exceptions import MessageNotFoundError


def create_message(db: Session, new_message: NewMessage) -> Message:
    return repository.create_message(db, new_message)


def get_message(db: Session, message_id: UUID) -> Message:
    msg = repository.get_message_by_id(db, message_id)
    if not msg:
        raise MessageNotFoundError(message_id)
    return msg


def list_messages_by_chat(db: Session, chat_id: UUID) -> list[Message]:
    return repository.get_messages_by_chat(db, chat_id)


def delete_message(db: Session, message_id: UUID) -> None:
    if not repository.delete_message(db, message_id):
        raise MessageNotFoundError(message_id)
