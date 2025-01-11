import aiohttp
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.core.config import settings
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate

class FinancialService:
    def __init__(self):
        self.api_key = settings.FINANCIAL_API_KEY
        self.base_url = "https://finnhub.io/api/v1"

    async def get_stock_price(self, ticker: str) -> Optional[float]:
        """Get real-time stock price for a given ticker."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/quote"
            params = {
                "symbol": ticker,
                "token": self.api_key
            }
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("c")  # Current price
                    return None
            except Exception as e:
                print(f"Error fetching stock price: {e}")
                return None

    async def get_company_news(self, ticker: str) -> list[Dict[str, Any]]:
        """Get latest news for a company."""
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/company-news"
            params = {
                "symbol": ticker,
                "token": self.api_key
            }
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    return []
            except Exception as e:
                print(f"Error fetching company news: {e}")
                return []

    async def get_portfolios(
        self, 
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Portfolio]:
        """Get all portfolios for a specific user."""
        return (
            db.query(Portfolio)
            .filter(Portfolio.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    async def get_portfolio(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int
    ) -> Optional[Portfolio]:
        """Get a specific portfolio by ID."""
        return (
            db.query(Portfolio)
            .filter(Portfolio.id == portfolio_id, Portfolio.user_id == user_id)
            .first()
        )

    async def create_portfolio(
        self, 
        db: Session, 
        portfolio: PortfolioCreate, 
        user_id: int
    ) -> Portfolio:
        """Create a new portfolio entry."""
        current_price = await self.get_stock_price(portfolio.ticker)
        
        db_portfolio = Portfolio(
            **portfolio.model_dump(),
            user_id=user_id,
            current_price=current_price or portfolio.purchase_price
        )
        db.add(db_portfolio)
        db.commit()
        db.refresh(db_portfolio)
        return db_portfolio

    async def update_portfolio(
        self,
        db: Session,
        portfolio_id: int,
        portfolio_update: PortfolioUpdate,
        user_id: int
    ) -> Portfolio:
        """Update a portfolio."""
        db_portfolio = await self.get_portfolio(db, portfolio_id, user_id)
        if not db_portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        update_data = portfolio_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_portfolio, field, value)

        # Update current price
        current_price = await self.get_stock_price(db_portfolio.ticker)
        if current_price:
            db_portfolio.current_price = current_price

        db.add(db_portfolio)
        db.commit()
        db.refresh(db_portfolio)
        return db_portfolio

    async def delete_portfolio(
        self,
        db: Session,
        portfolio_id: int,
        user_id: int
    ) -> bool:
        """Delete a portfolio."""
        db_portfolio = await self.get_portfolio(db, portfolio_id, user_id)
        if not db_portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")

        db.delete(db_portfolio)
        db.commit()
        return True

    async def update_portfolio_prices(self, db: Session) -> None:
        """Update current prices for all portfolios."""
        portfolios = db.query(Portfolio).all()
        for portfolio in portfolios:
            current_price = await self.get_stock_price(portfolio.ticker)
            if current_price:
                portfolio.current_price = current_price
        db.commit()