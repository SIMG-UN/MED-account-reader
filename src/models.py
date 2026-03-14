from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Float, Integer, JSON, DateTime, Text, func


class Base(DeclarativeBase):
    pass


class BancolombiaEcho(Base):
    __tablename__="bancolombia_echo"

    id = Column(Integer, primary_key=True)
    
    date = Column(String)
    body = Column(Text)
    create_at = Column(DateTime, server_default=func.now())











