from dataclasses import asdict
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import ExpenseSplitEntity
from .domain import ExpenseSplit, NewExpenseSplit, ExpenseSplitChanges


def _to_domain(entity: ExpenseSplitEntity) -> ExpenseSplit:
    return ExpenseSplit(
        id=entity.id,
        expense_id=entity.expense_id,
        contact_id=entity.contact_id,
        amount_owed=entity.amount_owed,
        status=entity.status,
        due_date=entity.due_date,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def create_split(db: Session, new_split: NewExpenseSplit) -> ExpenseSplit:
    entity = ExpenseSplitEntity(**asdict(new_split))
    db.add(entity)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def get_split_by_id(db: Session, split_id: UUID) -> ExpenseSplit | None:
    entity = db.get(ExpenseSplitEntity, split_id)
    return _to_domain(entity) if entity else None


def get_all_splits(db: Session) -> list[ExpenseSplit]:
    entities = db.scalars(select(ExpenseSplitEntity).order_by(ExpenseSplitEntity.created_at.desc())).all()
    return [_to_domain(e) for e in entities]


def get_splits_by_expense(db: Session, expense_id: UUID) -> list[ExpenseSplit]:
    entities = db.scalars(
        select(ExpenseSplitEntity).where(ExpenseSplitEntity.expense_id == expense_id).order_by(ExpenseSplitEntity.created_at.desc())
    ).all()
    return [_to_domain(e) for e in entities]


def update_split(db: Session, split_id: UUID, changes: ExpenseSplitChanges) -> ExpenseSplit | None:
    entity = db.get(ExpenseSplitEntity, split_id)
    if not entity:
        return None
    for key, value in asdict(changes).items():
        if value is not None:
            setattr(entity, key, value)
    db.flush()
    db.refresh(entity)
    return _to_domain(entity)


def delete_split(db: Session, split_id: UUID) -> bool:
    entity = db.get(ExpenseSplitEntity, split_id)
    if not entity:
        return False
    db.delete(entity)
    db.flush()
    return True
