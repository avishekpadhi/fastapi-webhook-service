
from fastapi import FastAPI
from .routes.webhook_routes import router as webhook_router
from .routes.transaction_routes import router as transaction_router

from datetime import datetime, timezone



app = FastAPI()
app.include_router(webhook_router)
app.include_router(transaction_router)

@app.get("/")
def health_check():
    return {
        "status": "HEALTHY",
        "current_time": datetime.now(timezone.utc).isoformat()
    }
