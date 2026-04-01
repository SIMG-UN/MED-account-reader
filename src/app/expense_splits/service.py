from uuid import UUID
from sqlalchemy.orm import Session
from . import repository
from .domain import ExpenseSplit, NewExpenseSplit, ExpenseSplitChanges
from ..exceptions import ExpenseSplitNotFoundError


def create_split(db: Session, new_split: NewExpenseSplit) -> ExpenseSplit:
    return repository.create_split(db, new_split)


def get_split(db: Session, split_id: UUID) -> ExpenseSplit:
    split = repository.get_split_by_id(db, split_id)
    if not split:
        raise ExpenseSplitNotFoundError(split_id)
    return split


def list_splits(db: Session) -> list[ExpenseSplit]:
    return repository.get_all_splits(db)


def list_splits_by_expense(db: Session, expense_id: UUID) -> list[ExpenseSplit]:
    return repository.get_splits_by_expense(db, expense_id)


def update_split(db: Session, split_id: UUID, changes: ExpenseSplitChanges) -> ExpenseSplit:
    split = repository.update_split(db, split_id, changes)
    if not split:
        raise ExpenseSplitNotFoundError(split_id)
    return split


def delete_split(db: Session, split_id: UUID) -> None:
    if not repository.delete_split(db, split_id):
        raise ExpenseSplitNotFoundError(split_id)
