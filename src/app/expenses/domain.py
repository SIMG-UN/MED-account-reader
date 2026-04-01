from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from decimal import Decimal


@dataclass
class Expense:
    id: UUID
    user_id: UUID
    title: str
    total_amount: Decimal
    currency: str
    type: str
    expense_date: datetime
    created_at: datetime
    updated_at: datetime
    description: str | None = None
    category: str | None = None
    merchant: str | None = None
    payment_method: str | None = None
    ai_notes: str | None = None


@dataclass
class NewExpense:
    user_id: UUID
    title: str
    total_amount: Decimal
    currency: str = "COP"
    type: str = "personal"
    description: str | None = None
    category: str | None = None
    merchant: str | None = None
    payment_method: str | None = None
    expense_date: datetime | None = None
    ai_notes: str | None = None


@dataclass
class ExpenseChanges:
    title: str | None = None
    description: str | None = None
    total_amount: Decimal | None = None
    currency: str | None = None
    category: str | None = None
    merchant: str | None = None
    type: str | None = None
    payment_method: str | None = None
    expense_date: datetime | None = None
    ai_notes: str | None = None
