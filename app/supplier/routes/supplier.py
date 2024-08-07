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


@router.get("/{id}", response_model=Supplier)
def get_supplier_by_id(
    id: int, service: SupplierService = Depends(get_supplier_service)
):
    return service.get_by_id(id=id)
