from sqlalchemy import Column, DateTime, Integer, func


class TableModel:
    id = Column(Integer, primary_key=True, autoincrement=True)

    updated_at = Column(
        DateTime(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    created_at = Column(
        DateTime(),
        server_default=func.now(),
        nullable=False,
    )
    deleted_at = Column(DateTime(), default=None)

    def __str__(self) -> str:
        return str(self.__dict__)
