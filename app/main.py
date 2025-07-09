# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import connect_to_mongo, close_mongo_connection
# --- CHANGE HERE: Imported the new 'categories' router ---
from app.api.v1.endpoints import products, categories

# FastAPI app instance
app = FastAPI(
    title="Trendify API",
    description="API for the Trendify e-commerce application.",
    version="1.0.0"
)

# --- Event Handlers ---
# These functions will run when the application starts and shuts down.
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


# --- Middleware ---
# CORS Set up to allow requests from our frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # The origin of our Next.js app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# --- API Routers ---
# --- products router ---
# Includes the products router with a prefix and tags for organization.
app.include_router(
    products.router,
    prefix="/api/v1/products",
    tags=["Products"]
)

# --- categories router ---
app.include_router(
    categories.router,
    prefix="/api/v1/categories",
    tags=["Categories"]
)


# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "Welcome to the Trendify API"}