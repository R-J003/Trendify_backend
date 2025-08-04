# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.database import connect_to_mongo, close_mongo_connection
from app.api.v1.endpoints import products, categories


# Lifespan Context Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await connect_to_mongo()
    yield
    print("Shutting down...")
    await close_mongo_connection()


# Create FastAPI app instance
app = FastAPI(
    title="Trendify API",
    description="API for the Trendify e-commerce application.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- THIS IS THE DEFINITIVE FIX ---
# This configuration tells the backend to accept requests from ANY origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)
# --------------------------------

# API Routers
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])


# Root and Health Check Endpoints
@app.get("/")
async def root():
    return {"message": "Welcome to the Trendify API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
