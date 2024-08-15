from fastapi import APIRouter
from app.catalog.routes import product, product_variety

router = APIRouter()

router.include_router(router=product.router, prefix="/product", tags=["product"])
router.include_router(
    router=product_variety.router, prefix="/product_variety", tags=["product_variety"]
)
