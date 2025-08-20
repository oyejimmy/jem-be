# filepath: app/schemas/product.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    full_name: Optional[str] = None
    type: Optional[str] = None
    retail_price: float
    offer_price: Optional[float] = None
    currency: str = "PKR"
    description: Optional[str] = None
    delivery_charges: float = 0.0
    stock: int = 0
    status: str = "available"
    images: Optional[str] = None
    available: int = 0
    sold: int = 0
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    full_name: Optional[str] = None
    type: Optional[str] = None
    retail_price: Optional[float] = None
    offer_price: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    delivery_charges: Optional[float] = None
    stock: Optional[int] = None
    status: Optional[str] = None
    images: Optional[str] = None
    available: Optional[int] = None
    sold: Optional[int] = None
    category_id: Optional[int] = None


class Product(ProductBase):
    id: int
    unique_key: str
    created_at: datetime

    class Config:
        from_attributes = True
