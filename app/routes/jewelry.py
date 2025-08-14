from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models import Product as ProductModel
from app.schemas.product import Product, ProductCreate
# from app.auth import get_current_user

jewelry_router = APIRouter()

@jewelry_router.get("/products", response_model=list[Product])
def read_products(db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    # Convert comma-separated string to list
    for product in products:
        product.images = product.images.split(",") if product.images else []
    return products

@jewelry_router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.images = product.images.split(",") if product.images else []
    return product

@jewelry_router.post("/products", response_model=Product)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    # user: str = Depends(get_current_user)
):
    # Exclude 'images' from dict to avoid duplicate
    product_data = product.dict(exclude={"images"})
    db_product = ProductModel(**product_data, images=",".join(product.images))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db_product.images = db_product.images.split(",") if db_product.images else []
    return db_product

@jewelry_router.put("/products/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    # user: str = Depends(get_current_user)
):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_data = product.dict(exclude={"images"})
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    db_product.images = ",".join(product.images)
    db.commit()
    db.refresh(db_product)
    db_product.images = db_product.images.split(",") if db_product.images else []
    return db_product

@jewelry_router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    # user: str = Depends(get_current_user)
):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}
