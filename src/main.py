from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

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
