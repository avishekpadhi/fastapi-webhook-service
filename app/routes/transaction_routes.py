from fastapi import APIRouter, Depends, HTTPException, status
from ..services.transaction_service import get_transaction_by_id
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db.db import get_db

router = APIRouter(prefix="/v1/transactions", tags=["transactions"])

@router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
def get_transaction_status(transaction_id: str, db: Session = Depends(get_db)):

    transaction = get_transaction_by_id(transaction_id, db)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction
