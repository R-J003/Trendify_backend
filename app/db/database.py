# backend/app/db/database.py
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

class Database:
    client: Optional[AsyncIOMotorClient] = None 
    db: Optional[AsyncIOMotorDatabase] = None 

db_handler = Database()

async def connect_to_mongo() -> None:
    """Connects to the MongoDB database."""
    print("Connecting to MongoDB...")
    db_handler.client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db_handler.db = db_handler.client[settings.MONGO_DB_NAME]
    print("Successfully connected to MongoDB.")

async def close_mongo_connection() -> None:
    """Closes the MongoDB connection."""
    print("Closing MongoDB connection...")
    if db_handler.client:
        db_handler.client.close()
    print("MongoDB connection closed.")

def get_database() -> AsyncIOMotorDatabase:
    """Returns the database instance."""
    if db_handler.db is None:
        raise Exception("Database has not been initialized. Call connect_to_mongo first.")
    return db_handler.db