from dataclasses import dataclass

from repository.transactions import TransactionsRepository
from schemas.transactions import TransactionCreate, TransactionRead

from exceptions import TransactionNotFoundException


@dataclass
class TransactionsService:
    transactions_repository: TransactionsRepository

    def get_transactions(self, offset: int = 0, limit: int = 0) -> list[TransactionRead]:
        transactions = [
            TransactionRead.model_validate(transaction, from_attributes=True) for transaction in
            self.transactions_repository.get_transactions(limit=limit, offset=offset)
        ]
        return transactions

    def create_transaction(self, transaction_schema: TransactionCreate) -> TransactionRead:
        transaction_id = self.transactions_repository.create_transaction(transaction_schema)
        transaction = self.transactions_repository.get_transaction(int(transaction_id))
        return TransactionRead.model_validate(transaction, from_attributes=True)

    def get_transaction(self, transaction_id: int) -> TransactionRead:
        transaction = self.transactions_repository.get_transaction(transaction_id)
        if not transaction:
            raise TransactionNotFoundException
        return TransactionRead.model_validate(transaction, from_attributes=True)
