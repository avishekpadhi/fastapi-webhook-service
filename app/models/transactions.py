from sqlalchemy import Column, String, Numeric, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    transaction_id = Column(String, nullable=False)
    source_account = Column(String, nullable=False)
    destination_account = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)
    currency = Column(String(3), nullable=False)
    status = Column(String, nullable=False)
