from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.db.session import get_db
from app.models import Product as ProductModel, Category
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.deps.auth import require_admin


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[Product])
def read_products(
    db: Session = Depends(get_db),
    category_name: Optional[str] = Query(None, description="Filter by category name (e.g., 'Rings')"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    status: Optional[str] = Query(None, description="Filter by status: available, out_of_stock, sold"),
    limit: Optional[int] = Query(100, description="Limit number of products returned"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
):
    """
    Get all products with optional filtering by category, status, and pagination.
    
    This is the MAIN API endpoint for your frontend table. Use this to display all products.
    
    Examples:
    - GET /products/ - Get all products (for frontend table)
    - GET /products/?category_name=Rings - Get all rings
    - GET /products/?category_id=1 - Get products from category ID 1
    - GET /products/?status=available - Get only available products
    - GET /products/?limit=10&offset=20 - Paginated results
    """
    query = db.query(ProductModel)
    
    # Filter by category name
    if category_name:
        query = query.join(Category).filter(Category.name.ilike(f"%{category_name}%"))
    
    # Filter by category ID
    if category_id:
        query = query.filter(ProductModel.category_id == category_id)
    
    # Filter by status
    if status:
        query = query.filter(ProductModel.status == status)
    
    # Apply pagination
    query = query.limit(limit).offset(offset)
    
    return query.all()


@router.get("/details/by-key/{unique_key}")
def get_product_details_by_key_for_order(unique_key: str, db: Session = Depends(get_db)):
    """
    Get detailed product information for order placement and WhatsApp contact by unique key.
    """
    product = db.query(ProductModel).join(Category).filter(ProductModel.unique_key == unique_key).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return _format_product_details(product)


def _format_product_details(product):
    """Helper function to format product details for order placement and WhatsApp contact."""
    # Parse images JSON string to list
    images = []
    if product.images:
        try:
            images = json.loads(product.images)
        except:
            images = [product.images]
    
    # Calculate total price
    total_price = product.offer_price or product.retail_price
    if product.delivery_charges:
        total_price += product.delivery_charges
    
    # WhatsApp contact information
    whatsapp_phone = "+92-300-1234567"  # You can make this configurable
    whatsapp_message = f"Hi! I'm interested in {product.name} (Key: {product.unique_key}). "
    whatsapp_message += f"Price: {product.currency} {product.offer_price or product.retail_price}. "
    whatsapp_message += "Can you provide more details?"
    
    # Create WhatsApp URL
    whatsapp_url = f"https://wa.me/{whatsapp_phone.replace('-', '').replace('+', '')}?text={whatsapp_message.replace(' ', '%20')}"
    
    return {
        "product": {
            "id": product.id,
            "unique_key": product.unique_key,
            "name": product.name,
            "full_name": product.full_name,
            "type": product.type,
            "description": product.description,
            "retail_price": product.retail_price,
            "offer_price": product.offer_price,
            "currency": product.currency,
            "delivery_charges": product.delivery_charges,
            "stock": product.stock,
            "status": product.status,
            "images": images,
            "available": product.available,
            "sold": product.sold,
            "category": product.category.name if product.category else None,
            "created_at": product.created_at
        },
        "whatsapp_info": {
            "phone": whatsapp_phone,
            "message": whatsapp_message,
            "whatsapp_url": whatsapp_url
        },
        "order_info": {
            "total_price": total_price,
            "delivery_time": "2-3 business days",
            "payment_methods": ["Cash on Delivery", "Bank Transfer", "Online Payment"],
            "warranty": "1 year warranty",
            "return_policy": "7 days return policy"
        }
    }


@router.get("/details/{product_id}")
def get_product_details_for_order(product_id: int, db: Session = Depends(get_db)):
    """
    Get detailed product information for order placement and WhatsApp contact by ID.
    
    This endpoint provides all the information needed when a user clicks on a product
    to place an order or contact via WhatsApp.
    
    Returns:
    {
        "product": {
            "id": 1,
            "unique_key": "abc123-def456-ghi789",
            "name": "Diamond Ring",
            "full_name": "18K Gold Diamond Engagement Ring",
            "description": "Elegant ring with brilliant-cut diamond",
            "retail_price": 2500,
            "offer_price": 2000,
            "currency": "PKR",
            "delivery_charges": 200,
            "stock": 5,
            "status": "available",
            "images": ["ring1.jpg", "ring2.jpg"],
            "category": "Rings"
        },
        "whatsapp_info": {
            "phone": "+92-300-1234567",
            "message": "Hi! I'm interested in Diamond Ring (Key: abc123-def456-ghi789). Price: PKR 2000. Can you provide more details?",
            "whatsapp_url": "https://wa.me/923001234567?text=Hi! I'm interested in Diamond Ring (Key: abc123-def456-ghi789). Price: PKR 2000. Can you provide more details?"
        },
        "order_info": {
            "total_price": 2200,
            "delivery_time": "2-3 business days",
            "payment_methods": ["Cash on Delivery", "Bank Transfer", "Online Payment"]
        }
    }
    """
    product = db.query(ProductModel).join(Category).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return _format_product_details(product)


# Convenience endpoints for each category
@router.get("/rings", response_model=List[Product])
def read_rings(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of rings returned")
):
    """Get all rings (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%ring%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/pendants", response_model=List[Product])
def read_pendants(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of pendants returned")
):
    """Get all pendants (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%pendant%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/bracelets", response_model=List[Product])
def read_bracelets(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of bracelets returned")
):
    """Get all bracelets (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%bracelet%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/bangles", response_model=List[Product])
def read_bangles(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of bangles returned")
):
    """Get all bangles (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%bangle%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/anklets", response_model=List[Product])
def read_anklets(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of anklets returned")
):
    """Get all anklets (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%anklet%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/ear-studs", response_model=List[Product])
def read_ear_studs(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of ear studs returned")
):
    """Get all ear studs (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%ear stud%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/earrings", response_model=List[Product])
def read_earrings(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of earrings returned")
):
    """Get all earrings (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%earing%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/hoops", response_model=List[Product])
def read_hoops(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of hoops returned")
):
    """Get all hoops (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%hoop%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/hair-accessories", response_model=List[Product])
def read_hair_accessories(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of hair accessories returned")
):
    """Get all hair accessories (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%hair%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/wall-frames", response_model=List[Product])
def read_wall_frames(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of wall frames returned")
):
    """Get all wall frames (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%wall frame%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/under-299", response_model=List[Product])
def read_under_299(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of products returned")
):
    """Get all products under 299 (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%under 299%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/combos", response_model=List[Product])
def read_combos(
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: Optional[int] = Query(100, description="Limit number of combos returned")
):
    """Get all combos (convenience endpoint)."""
    query = db.query(ProductModel).join(Category).filter(Category.name.ilike("%combo%"))
    
    if status:
        query = query.filter(ProductModel.status == status)
    
    return query.limit(limit).all()


@router.get("/by-key/{unique_key}", response_model=Product)
def read_product_by_key(unique_key: str, db: Session = Depends(get_db)):
    """Get a specific product by unique key."""
    product = db.query(ProductModel).filter(ProductModel.unique_key == unique_key).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID."""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=Product, dependencies=[Depends(require_admin)])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product (admin only).
    
    A unique key will be automatically generated for the new product.
    
    When you create a product, it will automatically appear in:
    - GET /products/ (main products list)
    - GET /products/{category_name} (if it matches the category)
    - GET /products/?category_name={category_name} (filtered results)
    """
    import uuid
    
    # Generate unique key for the new product
    product_data = product.dict()
    product_data['unique_key'] = str(uuid.uuid4())
    
    db_product = ProductModel(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/{product_id}", response_model=Product, dependencies=[Depends(require_admin)])
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """
    Update a product (admin only).
    
    When you update a product, the changes will automatically reflect in:
    - GET /products/ (main products list)
    - GET /products/{category_name} (if it matches the category)
    - GET /products/?category_name={category_name} (filtered results)
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", dependencies=[Depends(require_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product (admin only).
    
    When you delete a product, it will automatically be removed from:
    - GET /products/ (main products list)
    - GET /products/{category_name} (category-specific lists)
    - GET /products/?category_name={category_name} (filtered results)
    """
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}


