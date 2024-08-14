from app.common.database.database import Base
from app.common.models.table_model import TableModel


class AssetModel(Base, TableModel):
    __tablename__ = "asset"

    ...
