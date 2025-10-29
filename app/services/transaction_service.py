import time
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..models.transactions import Transaction

def process_transaction(payload: dict, db: Session):
    try:
        print("Starting transaction processing...")

        transaction_id = payload.get("transaction_id")

        existing = (
            db.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )
        if existing:
            if existing.status == "processed":
                return print(f"Transaction {transaction_id} already processed — skipping.")
            print(f"Updating pending transaction {transaction_id} to processed.")
        else:
            transaction = Transaction(
                transaction_id=transaction_id,
                source_account=payload.get("source_account"),
                destination_account=payload.get("destination_account"),
                amount=payload.get("amount"),
                currency=payload.get("currency"),
                status="processing",  
            )
            db.add(transaction)
            db.commit()
            print(f"Inserted pending transaction {transaction_id}...")

        #Simulate external API delay
        time.sleep(30)

        #Update to processed
        transaction = (
            db.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )
        transaction.status = "processed"
        transaction.processed_at = datetime.now(timezone.utc)
        db.commit()

        print(f"✅ Transaction {transaction_id} processed successfully.")

    except Exception as e:
        db.rollback()
        print("Error inserting transaction:", str(e))



def get_transaction_by_id(transaction_id: str, db: Session):

    transaction = (
        db.query(Transaction)
        .filter(Transaction.transaction_id == transaction_id)
        .first()
    )

    if not transaction:
        return None

    return {
        "transaction_id": transaction.transaction_id,
        "source_account": transaction.source_account,
        "destination_account": transaction.destination_account,
        "amount": transaction.amount,
        "currency": transaction.currency,
        "status": transaction.status,
        "processed_at": getattr(transaction, "processed_at", None),  
    }