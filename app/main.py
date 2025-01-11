from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
<<<<<<< HEAD
from app.api.v1.router import router as api_router
from app.db.base_class import Base
from app.db.session import engine

# Create tables
Base.metadata.create_all(bind=engine)
=======
from app.api.v1.router import api_router
>>>>>>> 1057750b7e20d3b20fee5059f81006ae529d5914

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

<<<<<<< HEAD
=======
# CORS middleware
>>>>>>> 1057750b7e20d3b20fee5059f81006ae529d5914
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
=======
# API router
>>>>>>> 1057750b7e20d3b20fee5059f81006ae529d5914
app.include_router(api_router, prefix=settings.API_V1_PREFIX)