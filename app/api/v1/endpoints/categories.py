# backend/app/api/v1/endpoints/categories.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Category(BaseModel):
    name: str
    imageUrl: str
    # No more productId! The frontend will handle the link.

# This is a simple list of the categories we want to display.
CATEGORIES_DATA = [
    {"name": "Dresses", "imageUrl": "/images/category-dresses.jpg"},
    {"name": "Tops", "imageUrl": "/images/category-tops.jpg"},
    {"name": "Casual Wear", "imageUrl": "/images/category-casual-wear.jpg"},
    {"name": "Shoes", "imageUrl": "/images/category-shoes.jpg"},
    {"name": "Accessories", "imageUrl": "/images/category-accessories.jpg"},
]

@router.get("/", response_model=List[Category])
async def list_categories():
    """
    Retrieve all product categories to display on the homepage.
    """
    return CATEGORIES_DATA