from dataclasses import asdict
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import PaymentEntity
from .domain import Payment, NewPayment, PaymentChanges


def _to_domain(entity: PaymentEntity) -> Payment:
    return Payment(
        id=entity.id,
        expense_split_id=entity.expense_split_id,
        amount_paid=entity.amount_paid,
        method=entity.method,
        paid_at=entity.paid_at,
        note=entity.note,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def create_payment(db: Session, new_payment: NewPayment) -> Payment:
    entity = PaymentEntity(**asdict(new_payment))
    db.add(entity)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def get_payment_by_id(db: Session, payment_id: UUID) -> Payment | None:
    entity = db.get(PaymentEntity, payment_id)
    return _to_domain(entity) if entity else None


def get_all_payments(db: Session) -> list[Payment]:
    entities = db.scalars(select(PaymentEntity).order_by(PaymentEntity.paid_at.desc())).all()
    return [_to_domain(e) for e in entities]


def get_payments_by_split(db: Session, split_id: UUID) -> list[Payment]:
    entities = db.scalars(
        select(PaymentEntity).where(PaymentEntity.expense_split_id == split_id).order_by(PaymentEntity.paid_at.desc())
    ).all()
    return [_to_domain(e) for e in entities]


def update_payment(db: Session, payment_id: UUID, changes: PaymentChanges) -> Payment | None:
    entity = db.get(PaymentEntity, payment_id)
    if not entity:
        return None
    for key, value in asdict(changes).items():
        if value is not None:
            setattr(entity, key, value)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def delete_payment(db: Session, payment_id: UUID) -> bool:
    entity = db.get(PaymentEntity, payment_id)
    if not entity:
        return False
    db.delete(entity)
    db.flush()
    return True
