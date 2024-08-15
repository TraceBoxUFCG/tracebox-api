import base64
from io import BytesIO
from typing import List
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
import qrcode
from sqlalchemy.orm import Session

from app.common.services.base import BaseService
from app.stock.repositories.asset import AssetRepository
from app.stock.schemas.asset import (
    Asset,
    AssetCreate,
    AssetGeneratePayload,
    AssetUpdate,
)
from xhtml2pdf import pisa


class AssetService(BaseService[AssetCreate, AssetUpdate, Asset]):
    db: Session
    repository: AssetRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=AssetRepository)
        self.db = db

    def generate_assets(self, payload: AssetGeneratePayload):
        quantity = payload.quantity
        created_assets: List[Asset] = [
            self.create(create=AssetCreate()) for _ in range(quantity)
        ]
        assets_id = [asset.id for asset in created_assets]

        return self.generate_assets_tags(list_of_ids=assets_id)

    def generate_assets_tags(self, list_of_ids: List[int]) -> BytesIO:
        qr_codes: List[tuple[str, int]] = [
            self.generate_qr_code(id=id) for id in list_of_ids
        ]

        return self.generate_asset_tag_pdf(qr_codes=qr_codes)

    def generate_qr_code(self, id: int) -> tuple[str, int]:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return (img_str, id)

    def generate_asset_tag_pdf(self, qr_codes: List[tuple[str, int]]) -> BytesIO:
        env = Environment(loader=FileSystemLoader("./templates"))
        template = env.get_template("tags_template.html")
        context = {"qr_codes": qr_codes}
        html = template.render(context)
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=pdf_buffer)

        if pisa_status.err:
            raise HTTPException(status_code=500, detail="Erro ao gerar tag de asset")

        pdf_buffer.seek(0)
        return pdf_buffer
