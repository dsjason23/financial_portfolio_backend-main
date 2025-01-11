# api/v1/endpoints/portfolio.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import portfolio as schema
from app.services import portfolio as service

router = APIRouter()

@router.get("/")
async def get_portfolios(db: Session = Depends(get_db)):
    return await service.get_portfolios(db)

@router.post("/")
async def create_portfolio(
    portfolio: schema.PortfolioCreate,
    db: Session = Depends(get_db)
):
    return await service.create_portfolio(db, portfolio)

@router.get("/{id}")
async def get_portfolio(id: int, db: Session = Depends(get_db)):
    portfolio = await service.get_portfolio(db, id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio

@router.put("/{id}")
async def update_portfolio(
    id: int,
    portfolio: schema.PortfolioUpdate,
    db: Session = Depends(get_db)
):
    return await service.update_portfolio(db, id, portfolio)

@router.delete("/{id}")
async def delete_portfolio(id: int, db: Session = Depends(get_db)):
    return await service.delete_portfolio(db, id)