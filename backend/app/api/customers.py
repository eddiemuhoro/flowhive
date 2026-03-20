from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.customers import Licence
from app.schemas.customers import (
    LicenceCreate,
    LicenceResponse,
    LicenceUpdate
)
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/companies", response_model=List[Dict])
async def get_companies(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get companies from external SAJSoft API
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://company.sajsoft.co.ke/?action=getareportscompanies"
            )
            response.raise_for_status()

            companies = response.json()
            return companies

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to fetch companies from external API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching companies: {str(e)}"
        )


@router.post("/licences")
async def create_licence(
    licence_payload: LicenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a licence"""
    licence = Licence(**licence_payload.model_dump())
    db.add(licence)
    db.commit()
    db.refresh(licence)
    return licence

@router.get("/licences", response_model=List[LicenceResponse])
async def get_licences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all licences"""
    licences = db.query(Licence).all()
    return licences

@router.patch("/licences/{licence_id}", response_model=LicenceResponse)
async def update_licence(
    licence_id: int,
    licence_payload: LicenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a licence"""
    licence = db.query(Licence).filter(Licence.id == licence_id).first()
    if not licence:
        raise HTTPException(status_code=404, detail="Licence not found")

    for key, value in licence_payload.model_dump(exclude_unset=True).items():
        setattr(licence, key, value)

    db.commit()
    db.refresh(licence)
    return licence

#put request to update licence
@router.put("/licences/{licence_id}", response_model=LicenceResponse)
async def replace_licence(
    licence_id: int,
    licence_payload: LicenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Replace a licence"""
    licence = db.query(Licence).filter(Licence.id == licence_id).first()
    if not licence:
        raise HTTPException(status_code=404, detail="Licence not found")

    for key, value in licence_payload.model_dump(exclude_unset=False).items():
        setattr(licence, key, value)

    db.commit()
    db.refresh(licence)
    return licence

@router.delete("/licences/{licence_id}")
async def delete_licence(
    licence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a licence"""
    licence = db.query(Licence).filter(Licence.id == licence_id).first()
    if not licence:
        raise HTTPException(status_code=404, detail="Licence not found")

    db.delete(licence)
    db.commit()
    return {"detail": "Licence deleted successfully"}