from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class ExpenseSplitCreate(BaseModel):
    expense_id: UUID
    contact_id: UUID
    amount_owed: Decimal
    status: str = "pending"
    due_date: datetime | None = None


class ExpenseSplitUpdate(BaseModel):
    amount_owed: Decimal | None = None
    status: str | None = None
    due_date: datetime | None = None


class ExpenseSplitResponse(BaseModel):
    id: UUID
    expense_id: UUID
    contact_id: UUID
    amount_owed: Decimal
    status: str
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
