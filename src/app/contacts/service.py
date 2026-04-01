from uuid import UUID
from sqlalchemy.orm import Session
from . import repository
from .domain import Contact, NewContact, ContactChanges
from ..exceptions import ContactNotFoundError


def create_contact(db: Session, new_contact: NewContact) -> Contact:
    return repository.create_contact(db, new_contact)


def get_contact(db: Session, contact_id: UUID) -> Contact:
    contact = repository.get_contact_by_id(db, contact_id)
    if not contact:
        raise ContactNotFoundError(contact_id)
    return contact


def list_contacts(db: Session) -> list[Contact]:
    return repository.get_all_contacts(db)


def list_contacts_by_user(db: Session, user_id: UUID) -> list[Contact]:
    return repository.get_contacts_by_user(db, user_id)


def update_contact(db: Session, contact_id: UUID, changes: ContactChanges) -> Contact:
    contact = repository.update_contact(db, contact_id, changes)
    if not contact:
        raise ContactNotFoundError(contact_id)
    return contact


def delete_contact(db: Session, contact_id: UUID) -> None:
    if not repository.delete_contact(db, contact_id):
        raise ContactNotFoundError(contact_id)
