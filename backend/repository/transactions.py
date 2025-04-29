

from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from sqlalchemy import func, select
from sqlalchemy.orm import sessionmaker

from annotations.transactions import TransactionID
from models import Transaction
from schemas.transactions import TransactionCreate


@dataclass
class TransactionsRepository:
    db_session: sessionmaker

    def get_transactions(self, offset: int = 0, limit: int = 0) -> list[Transaction]:
        query = select(Transaction).offset(offset).limit(limit).order_by(Transaction.date.desc())
        with self.db_session() as session:
            transactions: list[Transaction] = list(session.execute(query).scalars().all())
        return transactions

    def get_transactions_peer_month(self, year: int, month: int) -> list[Transaction]:
        query = select(Transaction).filter(
            func.date_trunc('month', Transaction.date) == datetime(year, month, 1)
        ).order_by(Transaction.date.desc())
        with self.db_session() as session:
            transactions: list[Transaction] = list(session.execute(query).scalars().all())
        return transactions


    def create_transaction(self, transaction_schema: TransactionCreate) -> TransactionID:
        transaction = Transaction(
            amount=transaction_schema.amount,
            category=transaction_schema.category,
            type=transaction_schema.type,
            comment=transaction_schema.comment,
            date=transaction_schema.date
        )
        with self.db_session() as session:
            session.add(transaction)
            session.flush()
            session.commit()
            transaction_id = transaction.id
        return TransactionID(transaction_id)

    def get_transaction(self, transation_id: int) -> Transaction | None:
        query = select(Transaction).where(Transaction.id == transation_id)
        with self.db_session() as session:
            transation = session.execute(query).scalar_one_or_none()
        return transation


