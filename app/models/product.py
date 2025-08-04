# backend/app/models/product.py
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId


# --- THIS IS THE Pydantic v1 COMPATIBLE PyObjectId CLASS ---
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# --- Pydantic Model for a Product (with v1 Config) ---
class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    price: float = Field(..., gt=0)
    description: str = Field(...)
    category: str = Field(...)
    imageUrl: str = Field(...)
    sizes: List[str] = Field(...)

    class Config:
        # Use the Pydantic v1 config keys
        allow_population_by_field_name = True
        arbitrary_types_allowed = True  # This is key for custom types in v1
        json_encoders = {ObjectId: str}
        schema_extra = {
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
