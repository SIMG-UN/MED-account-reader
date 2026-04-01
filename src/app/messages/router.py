from uuid import UUID
from fastapi import APIRouter, Depends
from ..database import db_dependency
from . import service
from .domain import NewMessage
from .schemas import MessageCreate, MessageResponse

router = APIRouter()


@router.post("/", response_model=MessageResponse, status_code=201)
def create_message(data: MessageCreate, conn=Depends(db_dependency)):
    return service.create_message(conn, NewMessage(chat_id=data.chat_id, role=data.role, content=data.content))


@router.get("/chat/{chat_id}", response_model=list[MessageResponse])
def list_messages_by_chat(chat_id: UUID, conn=Depends(db_dependency)):
    return service.list_messages_by_chat(conn, chat_id)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: UUID, conn=Depends(db_dependency)):
    return service.get_message(conn, message_id)


@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: UUID, conn=Depends(db_dependency)):
    service.delete_message(conn, message_id)
