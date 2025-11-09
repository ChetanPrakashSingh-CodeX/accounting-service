from sqlalchemy import Column, String, DateTime, Numeric, Integer
from sqlalchemy.sql import func
from database import Base

class Accounts(Base):
    __tablename__ = "Accounts"

    account_id = Column(Integer, primary_key=True)
    customer_id = Column(String(50), nullable=False, index=True)
    account_number = Column(Numeric(20, 0), nullable=False)
    account_type = Column(String(50), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())