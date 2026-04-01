from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from decimal import Decimal


@dataclass
class ExpenseSplit:
    id: UUID
    expense_id: UUID
    contact_id: UUID
    amount_owed: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
    due_date: datetime | None = None


@dataclass
class NewExpenseSplit:
    expense_id: UUID
    contact_id: UUID
    amount_owed: Decimal
    status: str = "pending"
    due_date: datetime | None = None


@dataclass
class ExpenseSplitChanges:
    amount_owed: Decimal | None = None
    status: str | None = None
    due_date: datetime | None = None
