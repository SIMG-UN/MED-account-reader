from uuid import UUID
from fastapi import APIRouter, Depends
from ..database import db_dependency
from . import service
from .domain import NewPayment, PaymentChanges
from .schemas import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter()


@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(data: PaymentCreate, conn=Depends(db_dependency)):
    return service.create_payment(conn, NewPayment(
        expense_split_id=data.expense_split_id,
        amount_paid=data.amount_paid,
        method=data.method,
        paid_at=data.paid_at,
        note=data.note,
    ))


@router.get("/", response_model=list[PaymentResponse])
def list_payments(conn=Depends(db_dependency)):
    return service.list_payments(conn)


@router.get("/split/{split_id}", response_model=list[PaymentResponse])
def list_payments_by_split(split_id: UUID, conn=Depends(db_dependency)):
    return service.list_payments_by_split(conn, split_id)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: UUID, conn=Depends(db_dependency)):
    return service.get_payment(conn, payment_id)


@router.patch("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: UUID, data: PaymentUpdate, conn=Depends(db_dependency)):
    return service.update_payment(conn, payment_id, PaymentChanges(
        amount_paid=data.amount_paid,
        method=data.method,
        paid_at=data.paid_at,
        note=data.note,
    ))


@router.delete("/{payment_id}", status_code=204)
def delete_payment(payment_id: UUID, conn=Depends(db_dependency)):
    service.delete_payment(conn, payment_id)
