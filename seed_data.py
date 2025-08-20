from typing import Dict, List
import json

from app.db.session import SessionLocal, init_db
from app.models import Category, Product, User, Order, OrderItem
from app.core.security import get_password_hash


def get_or_create_category(db, name: str) -> Category:
    cat = db.query(Category).filter(Category.name == name).first()
    if cat:
        return cat
    cat = Category(name=name)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def get_or_create_user(db, email: str, full_name: str, password: str, is_admin: bool = False) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    user = User(
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        is_admin=is_admin,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_product(
    db,
    name: str,
    full_name: str = None,
    type: str = None,
    retail_price: float = 0.0,
    offer_price: float = None,
    currency: str = "PKR",
    description: str = None,
    delivery_charges: float = 0.0,
    stock: int = 0,
    status: str = "available",
    images: List[str] = None,
    available: int = 0,
    sold: int = 0,
    category_id: int = None,
) -> Product:
    prod = db.query(Product).filter(Product.name == name).first()
    if prod:
        return prod
    
    # Convert images list to JSON string
    images_json = json.dumps(images) if images else None
    
    prod = Product(
        name=name,
        full_name=full_name,
        type=type,
        retail_price=retail_price,
        offer_price=offer_price,
        currency=currency,
        description=description,
        delivery_charges=delivery_charges,
        stock=stock,
        status=status,
        images=images_json,
        available=available,
        sold=sold,
        category_id=category_id,
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod


def create_order(
    db,
    items: List[Dict],
    customer_name: str,
    email: str,
    phone: str,
    address_line1: str,
    city: str,
    country: str,
    user_id: int | None = None,
) -> Order:
    order = Order(
        user_id=user_id,
        customer_name=customer_name,
        email=email,
        phone=phone,
        address_line1=address_line1,
        city=city,
        country=country,
    )
    total = 0.0
    for it in items:
        line_total = it["unit_price"] * it["quantity"]
        total += line_total
        order.items.append(
            OrderItem(
                product_id=it["product_id"],
                name=it["name"],
                unit_price=it["unit_price"],
                quantity=it["quantity"],
                line_total=line_total,
            )
        )
    order.total_amount = total
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def run() -> None:
    init_db()
    db = SessionLocal()
    try:
        # Users
        admin = get_or_create_user(db, "admin@example.com", "Admin User", "Admin@123", is_admin=True)
        customer = get_or_create_user(db, "customer@example.com", "Customer One", "Customer@123", is_admin=False)

        # Categories
        category_names = [
            "Rings",
            "Pendants",
            "Bracelets",
            "Bangles",
            "Anklets",
            "Ear Studs",
            "Earings",
            "Hoops",
            "Hair Accessories",
            "Wall Frame",
            "Under 299",
            "Combos",
        ]
        name_to_category: Dict[str, Category] = {name: get_or_create_category(db, name) for name in category_names}

        # Products with enhanced data
        products = [
            {
                "name": "Gold Zircon Bands Ring",
                "full_name": "18K Gold Zircon Bands Ring with Elegant Design",
                "type": "Ring",
                "retail_price": 650.0,
                "offer_price": 550.0,
                "currency": "PKR",
                "description": "Elegant zircon band ring with beautiful gold finish.",
                "delivery_charges": 100.0,
                "stock": 10,
                "status": "available",
                "images": ["gold_ring_1.jpg", "gold_ring_2.jpg", "gold_ring_3.jpg"],
                "available": 25,
                "sold": 15,
                "category_id": name_to_category["Rings"].id,
            },
            {
                "name": "Roman Black Dot Bracelet",
                "full_name": "Silver Roman Black Dot Designer Bracelet",
                "type": "Bracelet",
                "retail_price": 750.0,
                "offer_price": 650.0,
                "currency": "PKR",
                "description": "Stylish bracelet with roman black dot design.",
                "delivery_charges": 150.0,
                "stock": 5,
                "status": "available",
                "images": ["bracelet_1.jpg", "bracelet_2.jpg"],
                "available": 15,
                "sold": 10,
                "category_id": name_to_category["Bracelets"].id,
            },
            {
                "name": "Zircon Butterfly Ring",
                "full_name": "Silver Zircon Butterfly Design Ring",
                "type": "Ring",
                "retail_price": 500.0,
                "offer_price": 450.0,
                "currency": "PKR",
                "description": "Beautiful butterfly design ring with zircon stones.",
                "delivery_charges": 100.0,
                "stock": 0,
                "status": "out_of_stock",
                "images": ["butterfly_ring_1.jpg"],
                "available": 20,
                "sold": 20,
                "category_id": name_to_category["Rings"].id,
            },
            {
                "name": "Zirconia Designer Crown Ring",
                "full_name": "Gold Zirconia Designer Crown Ring",
                "type": "Ring",
                "retail_price": 600.0,
                "offer_price": 500.0,
                "currency": "PKR",
                "description": "Designer crown ring with zirconia stones.",
                "delivery_charges": 120.0,
                "stock": 8,
                "status": "available",
                "images": ["crown_ring_1.jpg", "crown_ring_2.jpg"],
                "available": 30,
                "sold": 22,
                "category_id": name_to_category["Rings"].id,
            },
            {
                "name": "Silver Hoop",
                "full_name": "Classic Silver Hoop Earrings",
                "type": "Hoop",
                "retail_price": 350.0,
                "offer_price": 299.0,
                "currency": "PKR",
                "description": "Classic silver hoop earrings for everyday wear.",
                "delivery_charges": 80.0,
                "stock": 20,
                "status": "available",
                "images": ["hoop_1.jpg", "hoop_2.jpg", "hoop_3.jpg"],
                "available": 50,
                "sold": 30,
                "category_id": name_to_category["Hoops"].id,
            },
        ]
        
        created_products: Dict[str, Product] = {}
        for product_data in products:
            prod = get_or_create_product(db, **product_data)
            created_products[product_data["name"]] = prod

        # Guest order
        create_order(
            db,
            items=[
                {
                    "product_id": created_products["Gold Zircon Bands Ring"].id,
                    "name": "Gold Zircon Bands Ring",
                    "unit_price": 550.0,
                    "quantity": 1,
                }
            ],
            customer_name="Guest Buyer",
            email="guest@example.com",
            phone="+92-300-0000000",
            address_line1="Street 1, House 2",
            city="Karachi",
            country="PK",
            user_id=None,
        )

        # Customer order
        create_order(
            db,
            items=[
                {
                    "product_id": created_products["Roman Black Dot Bracelet"].id,
                    "name": "Roman Black Dot Bracelet",
                    "unit_price": 650.0,
                    "quantity": 1,
                },
                {
                    "product_id": created_products["Silver Hoop"].id,
                    "name": "Silver Hoop",
                    "unit_price": 299.0,
                    "quantity": 2,
                },
            ],
            customer_name=customer.full_name or "Customer One",
            email=customer.email,
            phone="+92-311-1111111",
            address_line1="Street 10, House 20",
            city="Lahore",
            country="PK",
            user_id=customer.id,
        )

        print("✅ Seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    run()


