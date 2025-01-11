from fastapi import APIRouter
from .endpoints import portfolio, sentiment, users

router = APIRouter()

router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
router.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
router.include_router(users.router, prefix="/users", tags=["users"])