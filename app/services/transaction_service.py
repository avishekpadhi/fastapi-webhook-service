from sqlalchemy.orm import Session
from ..models.transactions import Transaction

def process_transaction(payload: dict, db: Session):
    """
    Handles inserting a transaction record into the database.
    This is your 'business logic layer' — decoupled from routing.
    """
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
        db.rollback()  # always rollback on errors
        print("❌ Error inserting transaction:", str(e))
