from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProductBase(BaseModel):
    name: str
    type: str
    full_name: str
    retail_price: float
    offer_price: float
    currency: str
    description: Optional[str] = None
    delivery_charges: Optional[float] = None
    stock: Optional[int] = None
    images: List[str]
    available: Optional[int] = 0
    sold: Optional[int] = 0
    status: Optional[str] = "available"  # "available" or "sold"

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class Anklet(Base):
    __tablename__ = "anklets"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Bangle(Base):
    __tablename__ = "bangle"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Bracelet(Base):
    __tablename__ = "bracelet"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Combo(Base):
    __tablename__ = "combo"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Earstud(Base):
    __tablename__ = "earstud"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Earing(Base):
    __tablename__ = "earing"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Hoop(Base):
    __tablename__ = "hoop"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Pendant(Base):
    __tablename__ = "pendant"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Ring(Base):
    __tablename__ = "ring"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")
    
class WallFrame(Base):
    __tablename__ = "wallframe"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    full_name = Column(String)
    retail_price = Column(Float)
    offer_price = Column(Float)
    currency = Column(String)
    description = Column(Text)
    delivery_charges = Column(Float)
    stock = Column(Integer)
    images = Column(Text)  # Comma-separated URLs
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    status = Column(String, default="available")
    __mapper_args__ = {
        "polymorphic_identity": "product",
        "polymorphic_on": type
    }
    def __repr__(self):
        return f"<Product(name={self.name}, type={self.type}, full_name={self.full_name})>"
    def __str__(self):
        return f"{self.name} ({self.type}): {self.full_name} - {self.retail_price} {self.currency}"
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "full_name": self.full_name,
            "retail_price": self.retail_price,
            "offer_price": self.offer_price,
            "currency": self.currency,
            "description": self.description,
            "delivery_charges": self.delivery_charges,
            "stock": self.stock,
            "images": self.images.split(",") if self.images else [],
            "available": self.available,
            "sold": self.sold,
            "status": self.status
        }

