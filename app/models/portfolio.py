# models/portfolio.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
<<<<<<< HEAD
from app.db.base_class import Base
=======
from app.db.base import Base
>>>>>>> 1057750b7e20d3b20fee5059f81006ae529d5914

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ticker = Column(String, index=True)
    shares = Column(Integer)
    purchase_price = Column(Float)
    current_price = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="portfolios")
    sentiments = relationship("Sentiment", back_populates="portfolio")
    news = relationship("News", back_populates="portfolio")