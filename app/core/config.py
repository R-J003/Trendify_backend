# backend/app/core/config.py
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017") #Deployed || Locally
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "trendify")
    
    # Port configuration for deployment
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Configuration for CORS (Cross-Origin Resource Sharing)
    # In a production environment, you should restrict this to your frontend's domain
    CLIENT_ORIGIN_URL: str = os.getenv("CLIENT_ORIGIN_URL", "https://trendify-frontend-two.vercel.app/")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
