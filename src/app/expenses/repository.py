from dataclasses import asdict
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import ExpenseEntity
from .domain import Expense, NewExpense, ExpenseChanges


def _to_domain(entity: ExpenseEntity) -> Expense:
    return Expense(
        id=entity.id,
        user_id=entity.user_id,
        title=entity.title,
        description=entity.description,
        total_amount=entity.total_amount,
        currency=entity.currency,
        category=entity.category,
        merchant=entity.merchant,
        type=entity.type,
        payment_method=entity.payment_method,
        expense_date=entity.expense_date,
        ai_notes=entity.ai_notes,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def create_expense(db: Session, new_expense: NewExpense) -> Expense:
    entity = ExpenseEntity(**asdict(new_expense))
    db.add(entity)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def get_expense_by_id(db: Session, expense_id: UUID) -> Expense | None:
    entity = db.get(ExpenseEntity, expense_id)
    return _to_domain(entity) if entity else None


def get_all_expenses(db: Session) -> list[Expense]:
    entities = db.scalars(select(ExpenseEntity).order_by(ExpenseEntity.expense_date.desc())).all()
    return [_to_domain(e) for e in entities]


def get_expenses_by_user(db: Session, user_id: UUID) -> list[Expense]:
    entities = db.scalars(
        select(ExpenseEntity).where(ExpenseEntity.user_id == user_id).order_by(ExpenseEntity.expense_date.desc())
    ).all()
    return [_to_domain(e) for e in entities]


def update_expense(db: Session, expense_id: UUID, changes: ExpenseChanges) -> Expense | None:
    entity = db.get(ExpenseEntity, expense_id)
    if not entity:
        return None
    for key, value in asdict(changes).items():
        if value is not None:
            setattr(entity, key, value)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def delete_expense(db: Session, expense_id: UUID) -> bool:
    entity = db.get(ExpenseEntity, expense_id)
    if not entity:
        return False
    db.delete(entity)
    db.flush()
    return True
