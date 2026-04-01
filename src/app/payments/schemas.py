from uuid import UUID
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class PaymentCreate(BaseModel):
    expense_split_id: UUID
    amount_paid: Decimal
    method: str | None = None
    paid_at: datetime | None = None
    note: str | None = None


class PaymentUpdate(BaseModel):
    amount_paid: Decimal | None = None
    method: str | None = None
    paid_at: datetime | None = None
    note: str | None = None


class PaymentResponse(BaseModel):
    id: UUID
    expense_split_id: UUID
    amount_paid: Decimal
    method: str | None
    paid_at: datetime
    note: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
