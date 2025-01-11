from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.schemas import sentiment as schema
from app.services.sentiment import SentimentService
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()
sentiment_service = SentimentService()

@router.get("/analyze/{ticker}", response_model=Dict[str, Any])
async def analyze_sentiment(
    ticker: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze sentiment for a specific ticker"""
    return await sentiment_service.analyze_sentiment(ticker)

@router.get("/portfolio/{portfolio_id}", response_model=List[schema.Sentiment])
async def get_portfolio_sentiment(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sentiment analysis for a specific portfolio"""
    return await sentiment_service.get_portfolio_sentiment(db, portfolio_id, current_user.id)

@router.post("/refresh/{portfolio_id}", response_model=List[schema.Sentiment])
async def refresh_sentiment(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Refresh sentiment analysis for a portfolio"""
    return await sentiment_service.refresh_sentiment(db, portfolio_id, current_user.id)