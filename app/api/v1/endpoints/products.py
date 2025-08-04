# backend/app/api/v1/endpoints/products.py
from fastapi import APIRouter, HTTPException, status, Response
from typing import List
from bson import ObjectId

from app.db.database import get_database
from app.models.product import ProductInDB, ProductCreateModel, ProductUpdateModel

router = APIRouter()


def get_product_collection():
    db = get_database()
    return db.products


@router.get(
    "",  # Correct: Path is exactly the prefix
    response_description="List all products",
    response_model=List[ProductInDB],
)
async def list_products():
    collection = get_product_collection()
    products = await collection.find().to_list(100)
    return products


@router.get(
    "/{id}",
    response_description="Get a single product by its ID",
    response_model=ProductInDB,
)
async def show_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"{id} is not a valid ObjectId")
    collection = get_product_collection()
    product = await collection.find_one({"_id": ObjectId(id)})
    if product is None:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")
    return product


# === THIS IS THE FIX ===
# The path must be "" to match the URL /api/v1/products for POST requests.
@router.post(
    "",  # <-- FIX IS HERE
    response_description="Add new product",
    response_model=ProductInDB,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(product: ProductCreateModel):
    collection = get_product_collection()
    # Pydantic v2 uses model_dump()
    new_product = await collection.insert_one(product.model_dump())
    created_product = await collection.find_one({"_id": new_product.inserted_id})
    return created_product


@router.put(
    "/{id}", response_description="Update a product", response_model=ProductInDB
)
async def update_product(id: str, product_update: ProductUpdateModel):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"{id} is not a valid ObjectId")
    collection = get_product_collection()
    # Pydantic v2 uses model_dump(exclude_unset=True) for updates
    update_data = product_update.model_dump(exclude_unset=True)

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
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail=f"{id} is not a valid ObjectId")
    collection = get_product_collection()
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Product with ID {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
