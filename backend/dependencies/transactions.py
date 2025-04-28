from database import get_db_session
from repository import TransactionsRepository
from services import TransactionsService


def get_transactions_service() -> TransactionsService:
    return TransactionsService(
        get_transactions_repository()
    )

def get_transactions_repository() -> TransactionsRepository:
    return TransactionsRepository(
        get_db_session()
    )

