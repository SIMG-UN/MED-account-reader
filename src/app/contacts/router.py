from uuid import UUID
from fastapi import APIRouter, Depends
from ..database import db_dependency
from . import service
from .domain import NewContact, ContactChanges
from .schemas import ContactCreate, ContactUpdate, ContactResponse

router = APIRouter()


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(data: ContactCreate, conn=Depends(db_dependency)):
    return service.create_contact(conn, NewContact(user_id=data.user_id, name=data.name, email=data.email, phone=data.phone))


@router.get("/", response_model=list[ContactResponse])
def list_contacts(conn=Depends(db_dependency)):
    return service.list_contacts(conn)


@router.get("/user/{user_id}", response_model=list[ContactResponse])
def list_contacts_by_user(user_id: UUID, conn=Depends(db_dependency)):
    return service.list_contacts_by_user(conn, user_id)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: UUID, conn=Depends(db_dependency)):
    return service.get_contact(conn, contact_id)


@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: UUID, data: ContactUpdate, conn=Depends(db_dependency)):
    return service.update_contact(conn, contact_id, ContactChanges(name=data.name, email=data.email, phone=data.phone))


@router.delete("/{contact_id}", status_code=204)
def delete_contact(contact_id: UUID, conn=Depends(db_dependency)):
    service.delete_contact(conn, contact_id)
