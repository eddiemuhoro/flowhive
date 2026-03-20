from pydantic import BaseModel
from datetime import date
from typing import Optional

class LicenceCreate(BaseModel):
    customer_id: str
    customer_name: str
    licence_number: str
    issued_on: date
    expires_on: date
    notes: Optional[str] = None

class LicenceUpdate(BaseModel):
    """Schema for updating a licence"""
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    licence_number: Optional[str] = None
    issued_on: Optional[date] = None
    expires_on: Optional[date] = None
    notes: Optional[str] = None

class LicenceResponse(LicenceCreate):
    id: int

    class Config:
        from_attributes = True