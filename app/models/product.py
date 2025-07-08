# backend/app/models/product.py
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

# Pydantic doesn't have a native ObjectId type, so we create a custom one.
# This allows us to validate that a string is a valid ObjectId and
# also helps with JSON serialization.
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


class ProductModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    price: float = Field(..., gt=0) # Price must be greater than 0
    description: str = Field(...)
    category: str = Field(...)
    imageUrl: str = Field(...)
    sizes: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Summer Dress",
                "price": 49.99,
                "description": "This elegant summer dress is perfect for sunny days.",
                "category": "Perfect for sunny days",
                "imageUrl": "/images/summer-dress.png",
                "sizes": ["S", "M", "L", "XL"]
            }
        }

# This model can be used when returning data from the database
class ProductInDB(ProductModel):
    pass