from fastapi import APIRouter

from app.api.v1.endpoints import products, categories, auth, orders


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(products.router)
api_router.include_router(categories.router)
api_router.include_router(auth.router)
api_router.include_router(orders.router)


