from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base  # 🔹 Ensure database.py exists

# 🔹 User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    plaid_access_token = Column(String, nullable=True)

# 🔹 Transaction Table
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    description = Column(String, nullable=True)

    user = relationship("User")
