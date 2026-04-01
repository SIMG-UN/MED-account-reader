from uuid import UUID
from fastapi import APIRouter, Depends
from ..database import db_dependency
from . import service
from .domain import NewChat, ChatChanges
from .schemas import ChatCreate, ChatUpdate, ChatResponse

router = APIRouter()


@router.post("/", response_model=ChatResponse, status_code=201)
def create_chat(data: ChatCreate, conn=Depends(db_dependency)):
    return service.create_chat(conn, NewChat(user_id=data.user_id, title=data.title))


@router.get("/", response_model=list[ChatResponse])
def list_chats(conn=Depends(db_dependency)):
    return service.list_chats(conn)


@router.get("/user/{user_id}", response_model=list[ChatResponse])
def list_chats_by_user(user_id: UUID, conn=Depends(db_dependency)):
    return service.list_chats_by_user(conn, user_id)


@router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: UUID, conn=Depends(db_dependency)):
    return service.get_chat(conn, chat_id)


@router.patch("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: UUID, data: ChatUpdate, conn=Depends(db_dependency)):
    return service.update_chat(conn, chat_id, ChatChanges(title=data.title))


@router.delete("/{chat_id}", status_code=204)
def delete_chat(chat_id: UUID, conn=Depends(db_dependency)):
    service.delete_chat(conn, chat_id)
