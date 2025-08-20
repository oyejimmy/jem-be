from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid


class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    unique_key = Column(String, unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    
    retail_price = Column(Float, nullable=False)
    offer_price = Column(Float, nullable=True)
    currency = Column(String, default="PKR")
    
    description = Column(Text, nullable=True)
    delivery_charges = Column(Float, default=0.0)
    
    stock = Column(Integer, default=0)
    status = Column(String, default="available")
    
    images = Column(Text, nullable=True)
    available = Column(Integer, default=0)
    sold = Column(Integer, default=0)
    
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    category = relationship("Category", back_populates="products")
