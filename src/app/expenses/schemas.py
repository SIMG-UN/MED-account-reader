from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    user_id: UUID
    title: str
    description: str | None = None
    total_amount: Decimal
    currency: str = "COP"
    category: str | None = None
    merchant: str | None = None
    type: str = "personal"
    payment_method: str | None = None
    expense_date: datetime | None = None
    ai_notes: str | None = None


class ExpenseUpdate(BaseModel):
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


class ExpenseResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str | None
    total_amount: Decimal
    currency: str
    category: str | None
    merchant: str | None
    type: str
    payment_method: str | None
    expense_date: datetime
    ai_notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
