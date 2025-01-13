from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import router as api_router
from app.db.base_class import Base
from app.db.session import engine

# Create tables
Base.metadata.create_all(bind=engine)

# Define metadata for API documentation
description = """
🚀 Financial Portfolio API

This API provides comprehensive portfolio management and financial analysis features:

### Features

* 👥 **Users** - User management and authentication
* 📊 **Portfolio Management** - Create and manage stock portfolios
* 📈 **Real-time Stock Data** - Live stock prices and updates
* 🔍 **Sentiment Analysis** - Market sentiment analysis based on news
* 📰 **News Integration** - Latest financial news for stocks

Try out the API using the interactive endpoints below!
"""

tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication operations. Get your access token here.",
    },
    {
        "name": "users",
        "description": "User management operations.",
    },
    {
        "name": "portfolio",
        "description": "Create and manage your stock portfolios. View real-time prices and performance.",
    },
    {
        "name": "sentiment",
        "description": "Analyze market sentiment based on news and trends.",
    }
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "operationsSorter": "method",
        "tagsSorter": "alpha",
        "docExpansion": "none"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)