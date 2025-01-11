from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas import portfolio as schema
from app.services import financial as service
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schema.Portfolio])
async def get_portfolios(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get all portfolios for the current user"""
    return await service.get_portfolios(db, current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=schema.Portfolio)
async def create_portfolio(
    portfolio: schema.PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await service.create_portfolio(
        db=db,
        portfolio=portfolio,
        user_id=current_user.id
    )