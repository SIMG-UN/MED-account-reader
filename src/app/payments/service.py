from uuid import UUID
from sqlalchemy.orm import Session
from . import repository
from .domain import Payment, NewPayment, PaymentChanges
from ..exceptions import PaymentNotFoundError


def create_payment(db: Session, new_payment: NewPayment) -> Payment:
    return repository.create_payment(db, new_payment)


def get_payment(db: Session, payment_id: UUID) -> Payment:
    payment = repository.get_payment_by_id(db, payment_id)
    if not payment:
        raise PaymentNotFoundError(payment_id)
    return payment


def list_payments(db: Session) -> list[Payment]:
    return repository.get_all_payments(db)


def list_payments_by_split(db: Session, split_id: UUID) -> list[Payment]:
    return repository.get_payments_by_split(db, split_id)


def update_payment(db: Session, payment_id: UUID, changes: PaymentChanges) -> Payment:
    payment = repository.update_payment(db, payment_id, changes)
    if not payment:
        raise PaymentNotFoundError(payment_id)
    return payment


def delete_payment(db: Session, payment_id: UUID) -> None:
    if not repository.delete_payment(db, payment_id):
        raise PaymentNotFoundError(payment_id)
