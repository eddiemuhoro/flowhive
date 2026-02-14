from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
import httpx
from app.models.user import User
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
