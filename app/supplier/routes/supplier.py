from fastapi import APIRouter, Depends
from fastapi_pagination import Page

from app.supplier.deps import get_supplier_service
from app.supplier.schemas.supplier import Supplier, SupplierCreate
from app.supplier.services.supplier import SupplierService
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter()


@router.post("/", response_model=Supplier)
def create_supplier(
    payload: SupplierCreate, service: SupplierService = Depends(get_supplier_service)
):
    return service.create(create=payload)


@router.get("/", response_model=Page[Supplier])
def get_all_suppliers(service: SupplierService = Depends(get_supplier_service)):
    return paginate(service.get_all_for_pagination())


@router.get("/{id}", response_model=Supplier)
def get_supplier_by_id(
    id: int, service: SupplierService = Depends(get_supplier_service)
):
    return service.get_by_id(id=id)


@router.delete("/{id}")
def delete_supplier(id: int, service: SupplierService = Depends(get_supplier_service)):
    return service.delete(id=id)
