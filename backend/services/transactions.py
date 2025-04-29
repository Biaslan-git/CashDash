from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime

from exceptions import TransactionNotFoundException
from repository.transactions import TransactionsRepository
from schemas.transactions import TransactionCreate, TransactionRead


@dataclass
class TransactionsService:
    transactions_repository: TransactionsRepository

    def get_transactions(self, offset: int = 0, limit: int = 0) -> list[TransactionRead]:
        transactions = [
            TransactionRead.model_validate(transaction, from_attributes=True) for transaction in
            self.transactions_repository.get_transactions(limit=limit, offset=offset)
        ]
        return transactions

    def get_transactions_peer_month_grouped_by_days(self, year: int, month: int) -> list[list[tuple[str, list[TransactionRead]]]]:
        month_transactions = self.get_transactions_peer_month(year, month)
        grouped_transactions = self.group_transactions_by_days(month_transactions)
        return grouped_transactions

    def get_transactions_peer_month(self, year: int, month: int) -> list[TransactionRead]:
        transactions = [
            TransactionRead.model_validate(transaction, from_attributes=True) for transaction in
            self.transactions_repository.get_transactions_peer_month(year, month)
        ]
        return transactions
    
    @staticmethod 
    def group_transactions_by_days(transactions: list[TransactionRead]) -> list[list[tuple[str, list[TransactionRead]]]]:
        # Сначала группируем транзакции по дням
        transactions_by_day = defaultdict(list)
        
        for transaction in transactions:
            # Получаем дату без времени (только день)
            day_key = transaction.date.strftime('%Y-%m-%d')
            transactions_by_day[day_key].append(transaction)
        
        # Преобразуем в нужный формат вывода
        result = []
        day_group = []
        
        for day, day_transactions in transactions_by_day.items():
            # Преобразуем транзакции в словари
            transactions_data = [
                TransactionRead(
                    id=t.id,
                    amount=t.amount,
                    type=t.type.value,  # Предполагаем, что TransactionType - это Enum
                    category=t.category,
                    comment=t.comment,
                    date=t.date
                )
                for t in day_transactions
            ]
            
            # Определяем название дня
            transaction_date = day_transactions[0].date
            if transaction_date.date() == datetime.now().date():
                day_name = 'Today'
            else:
                day_name = transaction_date.strftime('%d.%m.%Y')
            
            day_group.append((day_name, transactions_data))
        
        result.append(day_group)
        return result

    def create_transaction(self, transaction_schema: TransactionCreate) -> TransactionRead:
        transaction_id = self.transactions_repository.create_transaction(transaction_schema)
        transaction = self.transactions_repository.get_transaction(int(transaction_id))
        return TransactionRead.model_validate(transaction, from_attributes=True)

    def get_transaction(self, transaction_id: int) -> TransactionRead:
        transaction = self.transactions_repository.get_transaction(transaction_id)
        if not transaction:
            raise TransactionNotFoundException
        return TransactionRead.model_validate(transaction, from_attributes=True)
