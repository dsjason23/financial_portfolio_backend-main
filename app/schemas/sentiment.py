# schemas/sentiment.py
from pydantic import BaseModel
from datetime import datetime
from app.models.sentiment import SentimentType

class SentimentBase(BaseModel):
    sentiment_type: SentimentType
    confidence: float

class SentimentCreate(SentimentBase):
    portfolio_id: int

class Sentiment(SentimentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SentimentInDB(Sentiment):
    portfolio_id: int