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