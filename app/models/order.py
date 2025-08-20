from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Order(Base):
	__tablename__ = "orders"
	id = Column(Integer, primary_key=True, index=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
	customer_name = Column(String, nullable=False)
	email = Column(String, nullable=False)
	phone = Column(String, nullable=False)
	address_line1 = Column(String, nullable=False)
	address_line2 = Column(String, nullable=True)
	city = Column(String, nullable=False)
	postal_code = Column(String, nullable=True)
	country = Column(String, nullable=False)
	status = Column(String, default="pending")
	total_amount = Column(Float, default=0)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
	updated_at = Column(DateTime(timezone=True), onupdate=func.now())

	items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
	__tablename__ = "order_items"
	id = Column(Integer, primary_key=True, index=True)
	order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
	product_id = Column(Integer, nullable=False)
	name = Column(String, nullable=False)
	image_url = Column(String, nullable=True)
	unit_price = Column(Float, nullable=False)
	quantity = Column(Integer, nullable=False)
	line_total = Column(Float, nullable=False)

	order = relationship("Order", back_populates="items")


