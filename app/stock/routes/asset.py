from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi_pagination import Page

from app.stock.schemas.asset import Asset, AssetGeneratePayload, AssetListParams
from app.stock.services.asset import AssetService
from app.supplier.deps import get_asset_service
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter()


@router.post("/generate_tags/")
def generate_tags(
    payload: AssetGeneratePayload, service: AssetService = Depends(get_asset_service)
):
    tags_pdf = service.generate_assets(payload=payload)

    return StreamingResponse(
        tags_pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment;filename=qrcodes.pdf"},
    )


@router.get("/{id}/tag/")
def get_asset_tag(id: int, service: AssetService = Depends(get_asset_service)):
    tags_pdf = service.generate_assets_tags(list_of_ids=[id])

    return StreamingResponse(
        tags_pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment;filename=qrcodes.pdf"},
    )


@router.get("/", response_model=Page[Asset])
def get_all_tags(
    params: AssetListParams = Depends(),
    service: AssetService = Depends(get_asset_service),
):
    return paginate(service.get_all_for_pagination(params=params))
