# schemas/portfolio.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PortfolioBase(BaseModel):
    ticker: str
    shares: int
    purchase_price: float

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    shares: Optional[int] = None
    purchase_price: Optional[float] = None

class Portfolio(PortfolioBase):
    id: int
    user_id: int
    current_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PortfolioInDB(Portfolio):
    pass