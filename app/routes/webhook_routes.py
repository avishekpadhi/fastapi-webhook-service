from fastapi import APIRouter, Request, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db.db import get_db
from ..services.transaction_service import process_transaction


router = APIRouter(prefix="/v1/webhooks", tags=["webhooks"])

@router.post("/transactions", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    payload = await request.json()
    response = {"message": "Webhook received"}

    background_tasks.add_task(process_transaction, payload, db)
    return response


