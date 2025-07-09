# backend/app/db/seed.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "trendify")

# Data to seed the database
# The 'name' fields here should match with categories.py requirements.
products_data = [
    {
        "name": "Summer Dress",
        "price": 999,
        "description": "This elegant summer dress is perfect for sunny days...",
        "category": "Dresses",
        "imageUrl": "/images/summer-dress.png",
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "name": "Casual T-Shirt",
        "price": 1090.90,
        "description": "A classic and comfortable T-shirt for everyday wear...",
        "category": "Tops",
        "imageUrl": "/images/casual-t-shirt.png",
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "name": "Evening Gown",
        "price": 1199,
        "description": "An elegant gown perfect for special occasions...",
        "category": "Dresses",
        "imageUrl": "/images/evening-gown-1.jpg",
        "sizes": ["S", "M", "L"]
    },
    {
        "name": "Casual Wear",
        "price": 799,
        "description": "Comfortable and chic outfit for a casual day out...",
        "category": "Outfits",
        "imageUrl": "/images/casual-wear-1.jpg",
        "sizes": ["M", "L", "XL"]
    },
    {
        "name": "Flower Flask",
        "price": 599,
        "description": "Complete your look with our stylish Flower Flask...",
        "category": "Accessories",
        "imageUrl": "/images/flower-flask.jpg",
        "sizes": ["One Size"]
    },
    {
        "name": "Jeans",
        "price": 899,
        "description": "Classic straight-leg jeans made from durable, high-quality denim.",
        "category": "Casual Wear",
        "imageUrl": "/images/jeans.jpg",
        "sizes": ["28", "30", "32", "34", "36"]
    },
    {
        "name": "Kurti",
        "price": 1500,
        "description": "A beautifully embroidered kurti, perfect for both casual and festive occasions.",
        "category": "Tops",
        "imageUrl": "/images/kurti.jpg",
        "sizes": ["S", "M", "L", "XL"]
    },
    {
        "name": "Shoes",
        "price": 1200,
        "description": "Stylish and comfortable leather shoes to complete any outfit.",
        "category": "Shoes",
        "imageUrl": "/images/shoes.jpg",
        "sizes": ["5", "6", "7", "8", "9"]
    }
]

async def seed_db():
    client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    db = client[MONGO_DB_NAME]
    product_collection = db.products
    
    print("Starting database seed...")
    
    print(f"Deleting existing documents from '{MONGO_DB_NAME}.products'...")
    await product_collection.delete_many({})
    
    print(f"Inserting {len(products_data)} documents with corrected names...")
    result = await product_collection.insert_many(products_data)
    
    print(f"Successfully inserted {len(result.inserted_ids)} documents.")
    
    client.close()
    print("Database seed complete. Connection closed.")

if __name__ == "__main__":
    asyncio.run(seed_db())