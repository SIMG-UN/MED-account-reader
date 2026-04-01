from uuid import UUID, uuid4
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import String, DateTime, Text, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from .database import Base


class UserEntity(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    contacts: Mapped[list["ContactEntity"]] = relationship("ContactEntity", back_populates="user", cascade="all, delete-orphan")
    expenses: Mapped[list["ExpenseEntity"]] = relationship("ExpenseEntity", back_populates="user", cascade="all, delete-orphan")
    chats: Mapped[list["ChatEntity"]] = relationship("ChatEntity", back_populates="user", cascade="all, delete-orphan")


class ContactEntity(Base):
    __tablename__ = "contacts"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped[UserEntity] = relationship(UserEntity, back_populates="contacts")
    expense_splits: Mapped[list["ExpenseSplitEntity"]] = relationship("ExpenseSplitEntity", back_populates="contact", cascade="all, delete-orphan")


class ExpenseEntity(Base):
    __tablename__ = "expenses"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="COP")
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    merchant: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="personal")
    payment_method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    expense_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    ai_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped[UserEntity] = relationship(UserEntity, back_populates="expenses")
    splits: Mapped[list["ExpenseSplitEntity"]] = relationship("ExpenseSplitEntity", back_populates="expense", cascade="all, delete-orphan")


class ChatEntity(Base):
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    user: Mapped[UserEntity] = relationship(UserEntity, back_populates="chats")
    messages: Mapped[list["MessageEntity"]] = relationship("MessageEntity", back_populates="chat", cascade="all, delete-orphan")


class ExpenseSplitEntity(Base):
    __tablename__ = "expense_splits"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    expense_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False)
    contact_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False)
    amount_owed: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    due_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    expense: Mapped[ExpenseEntity] = relationship(ExpenseEntity, back_populates="splits")
    contact: Mapped[ContactEntity] = relationship(ContactEntity, back_populates="expense_splits")
    payments: Mapped[list["PaymentEntity"]] = relationship("PaymentEntity", back_populates="split", cascade="all, delete-orphan")


class PaymentEntity(Base):
    __tablename__ = "payments"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    expense_split_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("expense_splits.id", ondelete="CASCADE"), nullable=False)
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    method: Mapped[str | None] = mapped_column(String(50), nullable=True)
    paid_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    split: Mapped[ExpenseSplitEntity] = relationship(ExpenseSplitEntity, back_populates="payments")


class MessageEntity(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )

    chat: Mapped[ChatEntity] = relationship(ChatEntity, back_populates="messages")
