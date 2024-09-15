from sqlalchemy.orm import Session

from app.catalog.repositories.packaging import PackagingRepository
from app.catalog.schemas.packaging import Packaging, PackagingCreate, PackagingUpdate

from app.common.services.base import BaseService


class PackagingService(BaseService[PackagingCreate, PackagingUpdate, Packaging]):
    db: Session
    repository: PackagingRepository

    def __init__(self, db: Session):
        super().__init__(db=db, repository=PackagingRepository, return_model=Packaging)
        self.db = db
