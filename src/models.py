from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Float, Integer, Boolean, JSON, DateTime, Text, func


class Base(DeclarativeBase):
    pass


class BancolombiaEcho(Base):
    __tablename__="bancolombia_echo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    amount = Column(Float)
    date = Column(DateTime)
    entity = Column(String)
    is_spent = Column(Boolean)
    create_at = Column(DateTime, server_default=func.now())











