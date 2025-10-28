from fastapi import APIRouter, Request, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..models.transactions import Transaction
from ..db.db import get_db
from ..services.transaction_service import process_transaction


router = APIRouter(tags=["webhooks"])


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected ✅"}
    except Exception as e:
        return {"status": "error ❌", "details": str(e)}


@router.post("/transactions")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    payload = await request.json()
    response = {"message": "Webhook received"}

    background_tasks.add_task(process_transaction, payload, db)
    return response


