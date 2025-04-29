from fastapi import APIRouter


router = APIRouter(prefix='/api')

@router.get('/transactions_grouped')
def transactions_per_month_grouped_by_days():
    return 
