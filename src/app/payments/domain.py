from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from decimal import Decimal


@dataclass
class Payment:
    id: UUID
    expense_split_id: UUID
    amount_paid: Decimal
    paid_at: datetime
    created_at: datetime
    updated_at: datetime
    method: str | None = None
    note: str | None = None


@dataclass
class NewPayment:
    expense_split_id: UUID
    amount_paid: Decimal
    method: str | None = None
    paid_at: datetime | None = None
    note: str | None = None


@dataclass
class PaymentChanges:
    amount_paid: Decimal | None = None
    method: str | None = None
    paid_at: datetime | None = None
    note: str | None = None
