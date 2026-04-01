from uuid import UUID
from fastapi import APIRouter, Depends
from ..database import db_dependency
from . import service
from .domain import NewUser, UserChanges
from .schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, conn=Depends(db_dependency)):
    return service.create_user(conn, NewUser(first_name=data.first_name, last_name=data.last_name, email=data.email))


@router.get("/", response_model=list[UserResponse])
def list_users(conn=Depends(db_dependency)):
    return service.list_users(conn)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: UUID, conn=Depends(db_dependency)):
    return service.get_user(conn, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: UUID, data: UserUpdate, conn=Depends(db_dependency)):
    return service.update_user(conn, user_id, UserChanges(first_name=data.first_name, last_name=data.last_name, email=data.email))


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, conn=Depends(db_dependency)):
    service.delete_user(conn, user_id)
