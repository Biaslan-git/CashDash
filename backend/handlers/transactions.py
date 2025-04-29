from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_transactions_service
from exceptions.transactions import TransactionNotFoundException
from schemas import TransactionCreate, TransactionRead
from services import TransactionsService


router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.get("/")
def get_transactions(
    offset: int = 0, 
    limit: int = 100, 
    transactions_service: TransactionsService = Depends(get_transactions_service)
) -> list[TransactionRead]:
    return transactions_service.get_transactions(offset=offset, limit=limit)


@router.get("/peer_month_grouped_by_day")
def get_transactions_peer_month(
    year: int,
    month: int,
    transactions_service: TransactionsService = Depends(get_transactions_service)
) -> list[list[tuple[str, list[TransactionRead]]]]:
    return transactions_service.get_transactions_peer_month_grouped_by_days(year, month)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_schema: TransactionCreate, 
    transactions_service: TransactionsService = Depends(get_transactions_service)
) -> TransactionRead:
    transaction = transactions_service.create_transaction(transaction_schema)
    return transaction


@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    transactions_service: TransactionsService = Depends(get_transactions_service)
) -> TransactionRead:
    try:
        transaction = transactions_service.get_transaction(transaction_id)
    except TransactionNotFoundException:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

