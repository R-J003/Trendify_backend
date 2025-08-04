# backend/app/models/product.py
from pydantic import BaseModel, Field
from typing import List, Any, Optional
from bson import ObjectId
from pydantic_core.core_schema import CoreSchema


# --- Custom Pydantic Type for MongoDB's ObjectId (Pydantic v2 compatible) ---
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> CoreSchema:
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        return CoreSchema(
            "union",
            [
                CoreSchema("is-instance", ObjectId),
                CoreSchema("no-info-plain-validator", validate_from_str),
            ],
            serialization={"type": "to-string"},
        )


# --- Pydantic Model for a Product ---
class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    price: float = Field(..., gt=0)
    description: str = Field(...)
    category: str = Field(...)
    imageUrl: str = Field(...)
    sizes: List[str] = Field(...)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "Summer Dress",
                "price": 49.99,
                "description": "This elegant summer dress is perfect for sunny days.",
                "category": "Dresses",
                "imageUrl": "/images/summer-dress.png",
                "sizes": ["S", "M", "L", "XL"],
            }
        }


# --- Database Model ---
class ProductInDB(ProductModel):
    pass


# --- Models for CRUD Operations ---
class ProductCreateModel(BaseModel):
    name: str = Field(...)
    price: float = Field(..., gt=0)
    description: str = Field(...)
    category: str = Field(...)
    imageUrl: str = Field(...)
    sizes: List[str] = Field(...)


class ProductUpdateModel(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    description: Optional[str] = None
    category: Optional[str] = None
    imageUrl: Optional[str] = None
    sizes: Optional[List[str]] = None
