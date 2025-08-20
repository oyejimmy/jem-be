from pydantic import BaseModel, EmailStr
from typing import List, Optional


class OrderItemIn(BaseModel):
	product_id: int
	name: str
	image_url: Optional[str] = None
	unit_price: float
	quantity: int


class OrderCreate(BaseModel):
	customer_name: str
	email: EmailStr
	phone: str
	address_line1: str
	address_line2: Optional[str] = None
	city: str
	postal_code: Optional[str] = None
	country: str
	items: List[OrderItemIn]


class OrderItemOut(OrderItemIn):
	id: int
	line_total: float

	class Config:
		from_attributes = True


class OrderOut(BaseModel):
	id: int
	status: str
	total_amount: float
	customer_name: str
	email: EmailStr
	phone: str
	address_line1: str
	address_line2: Optional[str] = None
	city: str
	postal_code: Optional[str] = None
	country: str
	items: List[OrderItemOut]

	class Config:
		from_attributes = True


