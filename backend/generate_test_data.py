import random
from models.transactions import TransactionType
from repository import TransactionsRepository
from database import get_db_session
from schemas.transactions import TransactionCreate
from faker import Faker

tr = TransactionsRepository(get_db_session())

fake = Faker()

for _ in range(100):
    transaction = TransactionCreate(
        amount=fake.random_int(),
        category=fake.street_name(),
        type=random.choice([TransactionType.income, TransactionType.expense]),
        comment=random.choice([None, fake.text()]),
        date=fake.date_time_this_year()
    )
    tr.create_transaction(transaction)
