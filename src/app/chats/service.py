from uuid import UUID
from sqlalchemy.orm import Session
from . import repository
from .domain import Chat, NewChat, ChatChanges
from ..exceptions import ChatNotFoundError


def create_chat(db: Session, new_chat: NewChat) -> Chat:
    return repository.create_chat(db, new_chat)


def get_chat(db: Session, chat_id: UUID) -> Chat:
    chat = repository.get_chat_by_id(db, chat_id)
    if not chat:
        raise ChatNotFoundError(chat_id)
    return chat


def list_chats(db: Session) -> list[Chat]:
    return repository.get_all_chats(db)


def list_chats_by_user(db: Session, user_id: UUID) -> list[Chat]:
    return repository.get_chats_by_user(db, user_id)


def update_chat(db: Session, chat_id: UUID, changes: ChatChanges) -> Chat:
    chat = repository.update_chat(db, chat_id, changes)
    if not chat:
        raise ChatNotFoundError(chat_id)
    return chat


def delete_chat(db: Session, chat_id: UUID) -> None:
    if not repository.delete_chat(db, chat_id):
        raise ChatNotFoundError(chat_id)
