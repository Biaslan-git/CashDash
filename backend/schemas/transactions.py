from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import TransactionType

class TransactionBase(BaseModel):
    amount: float
    category: str
    type: TransactionType
    comment: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
