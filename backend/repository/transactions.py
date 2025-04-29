
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from annotations.transactions import TransactionID
from models import Transaction
from schemas.transactions import TransactionCreate


@dataclass
class TransactionsRepository:
    db_session: sessionmaker

    def get_transactions(self, offset: int = 0, limit: int = 0) -> list[Transaction]:
        query = select(Transaction).offset(offset).limit(limit)
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


