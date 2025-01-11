# models/news.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    title = Column(String)
    content = Column(Text)
    source = Column(String)
    url = Column(String)
    published_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio = relationship("Portfolio", back_populates="news")