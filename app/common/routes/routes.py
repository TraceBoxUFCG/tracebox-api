from fastapi import APIRouter
from app.supplier.routes import supplier

router = APIRouter()

router.include_router(router=supplier.router, prefix="/supplier", tags=["supplier"])
