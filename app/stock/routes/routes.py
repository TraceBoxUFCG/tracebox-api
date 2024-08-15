from fastapi import APIRouter
from app.stock.routes import asset

router = APIRouter()

router.include_router(router=asset.router, prefix="/asset", tags=["asset"])
