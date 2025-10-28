from fastapi import FastAPI, Request, BackgroundTasks
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .models import Transaction

from .db import get_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "connected ✅"}
    except Exception as e:
        return {"status": "error ❌", "details": str(e)}

@app.post("/v1/webhooks/transactions")
async def receive_webhook(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    payload = await request.json()
    
    response = {"message": "Webhook received"}
    
    background_tasks.add_task(process_transaction, payload, db)
    
    return response

def process_transaction(payload: dict, db: Session):
    try:
        transaction = Transaction(
            transaction_id=payload.get("transaction_id"),
            source_account=payload.get("source_account"),
            amount=payload.get("amount"),
            status=payload.get("status"),
        )
        db.add(transaction)
        db.commit()
        print("✅ Transaction stored successfully:", payload)
    except Exception as e:
        print("❌ Error inserting transaction:", str(e))
