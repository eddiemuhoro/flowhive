from app.database import Base
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

class Licence(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=True)
    licence_number = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    issued_on = Column(DateTime, nullable=False)
    expires_on = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
