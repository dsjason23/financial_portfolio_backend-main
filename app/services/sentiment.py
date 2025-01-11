# services/sentiment.py
from typing import List, Optional
import aiohttp
from sqlalchemy.orm import Session
from app.models.sentiment import Sentiment, SentimentType
from app.models.portfolio import Portfolio
from app.schemas.sentiment import SentimentCreate

class SentimentService:
    def __init__(self):
        self.base_url = "https://api.example.com/sentiment"  # Replace with actual sentiment API

    async def analyze_text(self, text: str) -> tuple[SentimentType, float]:
        """Analyze sentiment of text and return sentiment type and confidence."""
        # This is a placeholder implementation
        # In a real application, you would integrate with a sentiment analysis API
        # or use a machine learning model
        
        # Mock implementation
        import random
        sentiment_types = list(SentimentType)
        sentiment = random.choice(sentiment_types)
        confidence = random.uniform(0.6, 0.95)
        
        return sentiment, confidence

    async def analyze_news(self, news_text: str) -> Optional[Sentiment]:
        """Analyze sentiment from news text."""
        sentiment_type, confidence = await self.analyze_text(news_text)
        return {
            "sentiment_type": sentiment_type,
            "confidence": confidence
        }

    async def create_sentiment(
        self, 
        db: Session, 
        sentiment: SentimentCreate
    ) -> Sentiment:
        """Create a new sentiment entry."""
        db_sentiment = Sentiment(**sentiment.model_dump())
        db.add(db_sentiment)
        db.commit()
        db.refresh(db_sentiment)
        return db_sentiment

    async def get_portfolio_sentiment(
        self, 
        db: Session, 
        portfolio_id: int
    ) -> List[Sentiment]:
        """Get sentiment analysis for a portfolio."""
        return db.query(Sentiment)\
                .filter(Sentiment.portfolio_id == portfolio_id)\
                .order_by(Sentiment.created_at.desc())\
                .all()

    async def analyze_portfolio(
        self, 
        db: Session, 
        portfolio_id: int
    ) -> List[Sentiment]:
        """Analyze sentiment for a portfolio's current news."""
        from app.services import FinancialService
        financial_service = FinancialService()
        
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            return []
            
        # Get latest news
        news = await financial_service.get_company_news(portfolio.ticker)
        sentiments = []
        
        # Analyze each news item
        for item in news[:5]:  # Analyze last 5 news items
            sentiment_type, confidence = await self.analyze_text(
                f"{item.get('headline', '')} {item.get('summary', '')}"
            )
            
            db_sentiment = await self.create_sentiment(
                db,
                SentimentCreate(
                    portfolio_id=portfolio_id,
                    sentiment_type=sentiment_type,
                    confidence=confidence
                )
            )
            sentiments.append(db_sentiment)
            
        return sentiments