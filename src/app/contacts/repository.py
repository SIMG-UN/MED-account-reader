from dataclasses import asdict
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import ContactEntity
from .domain import Contact, NewContact, ContactChanges


def _to_domain(entity: ContactEntity) -> Contact:
    return Contact(
        id=entity.id,
        user_id=entity.user_id,
        name=entity.name,
        email=entity.email,
        phone=entity.phone,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def create_contact(db: Session, new_contact: NewContact) -> Contact:
    entity = ContactEntity(
        user_id=new_contact.user_id,
        name=new_contact.name,
        email=new_contact.email,
        phone=new_contact.phone,
    )
    db.add(entity)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def get_contact_by_id(db: Session, contact_id: UUID) -> Contact | None:
    entity = db.get(ContactEntity, contact_id)
    return _to_domain(entity) if entity else None


def get_all_contacts(db: Session) -> list[Contact]:
    entities = db.scalars(select(ContactEntity).order_by(ContactEntity.created_at.desc())).all()
    return [_to_domain(e) for e in entities]


def get_contacts_by_user(db: Session, user_id: UUID) -> list[Contact]:
    entities = db.scalars(
        select(ContactEntity).where(ContactEntity.user_id == user_id).order_by(ContactEntity.created_at.desc())
    ).all()
    return [_to_domain(e) for e in entities]


def update_contact(db: Session, contact_id: UUID, changes: ContactChanges) -> Contact | None:
    entity = db.get(ContactEntity, contact_id)
    if not entity:
        return None
    for key, value in asdict(changes).items():
        if value is not None:
            setattr(entity, key, value)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def delete_contact(db: Session, contact_id: UUID) -> bool:
    entity = db.get(ContactEntity, contact_id)
    if not entity:
        return False
    db.delete(entity)
    db.flush()
    return True
