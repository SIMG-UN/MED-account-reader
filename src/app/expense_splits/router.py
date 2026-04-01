from uuid import UUID
from fastapi import APIRouter, Depends
from ..database import db_dependency
from . import service
from .domain import NewExpenseSplit, ExpenseSplitChanges
from .schemas import ExpenseSplitCreate, ExpenseSplitUpdate, ExpenseSplitResponse

router = APIRouter()


@router.post("/", response_model=ExpenseSplitResponse, status_code=201)
def create_split(data: ExpenseSplitCreate, conn=Depends(db_dependency)):
    return service.create_split(conn, NewExpenseSplit(
        expense_id=data.expense_id,
        contact_id=data.contact_id,
        amount_owed=data.amount_owed,
        status=data.status,
        due_date=data.due_date,
    ))


@router.get("/", response_model=list[ExpenseSplitResponse])
def list_splits(conn=Depends(db_dependency)):
    return service.list_splits(conn)


@router.get("/expense/{expense_id}", response_model=list[ExpenseSplitResponse])
def list_splits_by_expense(expense_id: UUID, conn=Depends(db_dependency)):
    return service.list_splits_by_expense(conn, expense_id)


@router.get("/{split_id}", response_model=ExpenseSplitResponse)
def get_split(split_id: UUID, conn=Depends(db_dependency)):
    return service.get_split(conn, split_id)


@router.patch("/{split_id}", response_model=ExpenseSplitResponse)
def update_split(split_id: UUID, data: ExpenseSplitUpdate, conn=Depends(db_dependency)):
    return service.update_split(conn, split_id, ExpenseSplitChanges(
        amount_owed=data.amount_owed,
        status=data.status,
        due_date=data.due_date,
    ))


@router.delete("/{split_id}", status_code=204)
def delete_split(split_id: UUID, conn=Depends(db_dependency)):
    service.delete_split(conn, split_id)
