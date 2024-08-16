from fastapi import APIRouter
from app.purchases.routes import purchase_order

router = APIRouter()

router.include_router(
    router=purchase_order.router, prefix="/purchase_order", tags=["purchase_order"]
)
