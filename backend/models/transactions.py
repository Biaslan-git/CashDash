import enum
from datetime import datetime

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"

class Transaction(Base):
    __tablename__ = "transactions"

    amount: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(index=True)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    comment: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

