# backend/app/api/v1/endpoints/products.py
from fastapi import (APIRouter, HTTPException, status, Response)
from typing import List
from bson import ObjectId

from app.db.database import get_database
from app.models.product import ProductInDB, ProductCreateModel, ProductUpdateModel

router = APIRouter()

# Dependency to get the database collection
def get_product_collection():
    db = get_database()
    return db.products

@router.get(
    "",
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


@router.post(
    "/",
    response_description="Add new product",
    response_model=ProductInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(product: ProductCreateModel):
    """
    Create a new product.
    """
    collection = get_product_collection()
    new_product = await collection.insert_one(product.dict())
    created_product = await collection.find_one({"_id": new_product.inserted_id})
    return created_product


@router.put(
    "/{id}", response_description="Update a product", response_model=ProductInDB
)
async def update_product(id: str, product_update: ProductUpdateModel):
    """
    Update an existing product by its ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"{id} is not a valid ObjectId")

    collection = get_product_collection()

    # Create a dict of fields to update, excluding any that are None
    update_data = {k: v for k, v in product_update.dict().items() if v is not None}

    if len(update_data) >= 1:
        update_result = await collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )

        if update_result.matched_count == 0:
            raise HTTPException(
                status_code=404, detail=f"Product with ID {id} not found"
            )

    if (
        existing_product := await collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing_product

    raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")


@router.delete(
    "/{id}",
    response_description="Delete a product",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(id: str):
    """
    Delete a product by its ID.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"{id} is not a valid ObjectId")

    collection = get_product_collection()
    delete_result = await collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
