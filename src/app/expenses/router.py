from uuid import UUID
from fastapi import APIRouter, Depends
from ..database import db_dependency
from . import service
from .domain import NewExpense, ExpenseChanges
from .schemas import ExpenseCreate, ExpenseUpdate, ExpenseResponse

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(data: ExpenseCreate, conn=Depends(db_dependency)):
    return service.create_expense(conn, NewExpense(
        user_id=data.user_id,
        title=data.title,
        total_amount=data.total_amount,
        currency=data.currency,
        type=data.type,
        description=data.description,
        category=data.category,
        merchant=data.merchant,
        payment_method=data.payment_method,
        expense_date=data.expense_date,
        ai_notes=data.ai_notes,
    ))


@router.get("/", response_model=list[ExpenseResponse])
def list_expenses(conn=Depends(db_dependency)):
    return service.list_expenses(conn)


@router.get("/user/{user_id}", response_model=list[ExpenseResponse])
def list_expenses_by_user(user_id: UUID, conn=Depends(db_dependency)):
    return service.list_expenses_by_user(conn, user_id)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: UUID, conn=Depends(db_dependency)):
    return service.get_expense(conn, expense_id)


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: UUID, data: ExpenseUpdate, conn=Depends(db_dependency)):
    return service.update_expense(conn, expense_id, ExpenseChanges(
        title=data.title,
        description=data.description,
        total_amount=data.total_amount,
        currency=data.currency,
        category=data.category,
        merchant=data.merchant,
        type=data.type,
        payment_method=data.payment_method,
        expense_date=data.expense_date,
        ai_notes=data.ai_notes,
    ))


@router.delete("/{expense_id}", status_code=204)
def delete_expense(expense_id: UUID, conn=Depends(db_dependency)):
    service.delete_expense(conn, expense_id)
