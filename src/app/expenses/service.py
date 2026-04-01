from uuid import UUID
from sqlalchemy.orm import Session
from . import repository
from .domain import Expense, NewExpense, ExpenseChanges
from ..exceptions import ExpenseNotFoundError


def create_expense(db: Session, new_expense: NewExpense) -> Expense:
    return repository.create_expense(db, new_expense)


def get_expense(db: Session, expense_id: UUID) -> Expense:
    expense = repository.get_expense_by_id(db, expense_id)
    if not expense:
        raise ExpenseNotFoundError(expense_id)
    return expense


def list_expenses(db: Session) -> list[Expense]:
    return repository.get_all_expenses(db)


def list_expenses_by_user(db: Session, user_id: UUID) -> list[Expense]:
    return repository.get_expenses_by_user(db, user_id)


def update_expense(db: Session, expense_id: UUID, changes: ExpenseChanges) -> Expense:
    expense = repository.update_expense(db, expense_id, changes)
    if not expense:
        raise ExpenseNotFoundError(expense_id)
    return expense


def delete_expense(db: Session, expense_id: UUID) -> None:
    if not repository.delete_expense(db, expense_id):
        raise ExpenseNotFoundError(expense_id)
