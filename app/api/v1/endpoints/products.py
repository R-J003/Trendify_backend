# backend/app/api/v1/endpoints/products.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId

from app.db.database import get_database
from app.models.product import ProductInDB

router = APIRouter()

# Dependency to get the database collection
def get_product_collection():
    db = get_database()
    return db.products

@router.get(
    "/",
    response_description="List all products",
    response_model=List[ProductInDB],
    status_code=status.HTTP_200_OK
)
async def list_products():
    """
    Retrieve all products from the database.
    """
    collection = get_product_collection()
    products = await collection.find().to_list(100) # Limit to 100 products
    return products


@router.get(
    "/{id}",
    response_description="Get a single product by its ID",
    response_model=ProductInDB,
    status_code=status.HTTP_200_OK
)
async def show_product(id: str):
    """
    Retrieve a single product by its unique ID.
    This endpoint returns the product details for the specified ID.
    The ID is the MongoDB document's `_id`.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"{id} is not a valid ObjectId")
        
    collection = get_product_collection()
    product = await collection.find_one({"_id": ObjectId(id)})

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {id} not found"
        )
    return product