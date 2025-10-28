#app/main.py

from fastapi import FastAPI
from .routes.webhook_routes import router as webhook_router


app = FastAPI()
app.include_router(webhook_router)
