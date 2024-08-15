from uuid import UUID

from sqlalchemy import cast
import sqlalchemy
from sqlalchemy.orm import Session

from app.common.repositories.base import BaseFinder, BaseRepository
from app.stock.models.asset import AssetModel


class AssetFinder(BaseFinder[AssetModel]):
    @classmethod
    def get_instance(cls, db: Session):
        return cls(db.query(AssetModel).filter(AssetModel.deleted_at.is_(None)))

    def filtered_by_id_ilike(self, target: str):
        if target:
            return AssetFinder(
                (
                    self.base_query.filter(
                        cast(AssetModel.id, sqlalchemy.String).ilike(
                            f"%{target.strip()}%"
                        )
                    )
                )
            )
        return self

    def search_by_query_criterias(self, target: str):
        id_query = self.filtered_by_id_ilike(target=target).query

        return AssetFinder(id_query)


class AssetRepository(
    BaseRepository[AssetModel, UUID],
):
    finder: AssetFinder

    def __init__(self, db: Session):
        super().__init__(
            AssetModel.id,
            model_class=AssetModel,
            finder=AssetFinder,
            db=db,
        )
