from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.models import Category, Product
from app.deps.auth import require_admin


router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    """Get all category names."""
    categories = db.query(Category).all()
    return [c.name for c in categories]


@router.get("/with-counts")
def list_categories_with_counts(db: Session = Depends(get_db)):
    """
    Get all categories with product counts.
    
    Returns:
    [
        {
            "id": 1,
            "name": "Rings",
            "product_count": 3
        }
    ]
    """
    categories = db.query(
        Category.id,
        Category.name,
        func.count(Product.id).label("product_count")
    ).outerjoin(Product).group_by(Category.id, Category.name).all()
    
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "product_count": cat.product_count
        }
        for cat in categories
    ]


@router.post("/", dependencies=[Depends(require_admin)], response_model=str)
def create_category(name: str, db: Session = Depends(get_db)):
    """Create a new category (admin only)."""
    if db.query(Category).filter(Category.name == name).first():
        raise HTTPException(status_code=400, detail="Category already exists")
    
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category.name


