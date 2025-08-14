# filepath: app/schemas/product.py
from pydantic import BaseModel, validator
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    type: Optional[str] = None
    full_name: str
    retail_price: float
    offer_price: float
    currency: str
    description: Optional[str] = None
    delivery_charges: Optional[float] = None
    stock: Optional[int] = None
    images: Optional[List[str]] = []
    status: str = "available"

    @validator("type", pre=True, always=True)
    def set_default_type(cls, v, values):
        return v or values.get("name")

    @validator("images", pre=True, always=True)
    def convert_images_to_list(cls, v):
        # If v is a string (from DB), convert to list
        if isinstance(v, str):
            return [v]
        # If None, return empty list
        if v is None:
            return []
        return v


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
