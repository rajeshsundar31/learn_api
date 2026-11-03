from sqlalchemy import Integer, String, Column, ForeignKey, Date, DateTime, func
from database.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Expense(Base):
    __tablename__ = "Expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    note = Column(String)
    date = Column(Date, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)