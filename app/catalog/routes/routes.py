from fastapi import APIRouter
from app.catalog.routes import product

router = APIRouter()

router.include_router(router=product.router, prefix="/product", tags=["product"])
