from fastapi import APIRouter, Depends

from app.supplier.deps import get_supplier_service
from app.supplier.schemas.supplier import Supplier, SupplierCreate
from app.supplier.services.supplier import SupplierService


router = APIRouter()


@router.post("/", response_model=Supplier)
def create_supplier(
    payload: SupplierCreate, service: SupplierService = Depends(get_supplier_service)
):
    return service.create(create=payload)
