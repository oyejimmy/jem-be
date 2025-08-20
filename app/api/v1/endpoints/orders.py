from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Order, OrderItem
from app.schemas.order import OrderCreate, OrderOut
from app.deps.auth import require_admin


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderOut)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
	order = Order(
		customer_name=order_in.customer_name,
		email=order_in.email,
		phone=order_in.phone,
		address_line1=order_in.address_line1,
		address_line2=order_in.address_line2,
		city=order_in.city,
		postal_code=order_in.postal_code,
		country=order_in.country,
	)
	total = 0.0
	for it in order_in.items:
		line_total = it.unit_price * it.quantity
		total += line_total
		order.items.append(
			OrderItem(
				product_id=it.product_id,
				name=it.name,
				image_url=it.image_url,
				unit_price=it.unit_price,
				quantity=it.quantity,
				line_total=line_total,
			)
		)
	order.total_amount = total
	db.add(order)
	db.commit()
	db.refresh(order)
	return order


@router.get("/", response_model=List[OrderOut], dependencies=[Depends(require_admin)])
def list_orders(db: Session = Depends(get_db)):
	return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderOut, dependencies=[Depends(require_admin)])
def get_order(order_id: int, db: Session = Depends(get_db)):
	order = db.query(Order).filter(Order.id == order_id).first()
	if not order:
		raise HTTPException(status_code=404, detail="Order not found")
	return order


