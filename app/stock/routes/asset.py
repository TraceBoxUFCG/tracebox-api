from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.stock.schemas.asset import AssetGeneratePayload
from app.stock.services.asset import AssetService
from app.supplier.deps import get_asset_service

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


@router.get("{id}/tag/")
def get_asset_tag(id: int, service: AssetService = Depends(get_asset_service)):
    tags_pdf = service.generate_assets_tags(list_of_ids=[id])

    return StreamingResponse(
        tags_pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment;filename=qrcodes.pdf"},
    )
