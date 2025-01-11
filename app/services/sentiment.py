from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sentiment import Sentiment, SentimentType
from app.models.portfolio import Portfolio
from app.services.financial import FinancialService
from fastapi import HTTPException

class SentimentService:
    def __init__(self):
        self.financial_service = FinancialService()

    async def get_portfolio_sentiment(
        self, 
        db: Session, 
        portfolio_id: int,
        user_id: int
    ) -> List[Sentiment]:
        """Get sentiment analysis for a portfolio"""
        # Verify portfolio belongs to user
        portfolio = db.query(Portfolio).filter(
            Portfolio.id == portfolio_id,
            Portfolio.user_id == user_id
        ).first()
        
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        return db.query(Sentiment).filter(
            Sentiment.portfolio_id == portfolio_id
        ).order_by(Sentiment.created_at.desc()).all()

    async def analyze_sentiment(self, ticker: str) -> dict:
        """Analyze sentiment for a ticker symbol"""
        news = await self.financial_service.get_company_news(ticker)
        if not news:
            return {
                "sentiment_type": SentimentType.HOLD,
                "confidence": 0.5,
                "news_count": 0
            }
            
        # Simple sentiment analysis based on news volume
        sentiment_type = SentimentType.HOLD
        confidence = 0.5
        
        # Default sentiment value for news items
        news_sentiment = 1  # positive sentiment for this example
        
        if len(news) > 10:  # Lots of news might indicate strong movement
            sentiment_type = SentimentType.STRONG_BUY if news_sentiment > 0 else SentimentType.STRONG_SELL
            confidence = 0.8
        elif len(news) > 5:
            sentiment_type = SentimentType.BUY if news_sentiment > 0 else SentimentType.SELL
            confidence = 0.6

        return {
            "sentiment_type": sentiment_type,
            "confidence": confidence,
            "news_count": len(news)
        }

    async def refresh_sentiment(
        self, 
        db: Session, 
        portfolio_id: int,
        user_id: int
    ) -> List[Sentiment]:
        """Refresh sentiment analysis for a portfolio"""
        # Verify portfolio belongs to user
        portfolio = db.query(Portfolio).filter(
            Portfolio.id == portfolio_id,
            Portfolio.user_id == user_id
        ).first()
        
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        # Get new sentiment analysis
        analysis = await self.analyze_sentiment(portfolio.ticker)
        
        # Create new sentiment record
        sentiment = Sentiment(
            portfolio_id=portfolio_id,
            sentiment_type=analysis["sentiment_type"],
            confidence=analysis["confidence"]
        )
        
        db.add(sentiment)
        db.commit()
        db.refresh(sentiment)
        
        return await self.get_portfolio_sentiment(db, portfolio_id, user_id)