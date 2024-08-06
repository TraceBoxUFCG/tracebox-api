from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.common.core.settings import settings
from sqlalchemy.ext.declarative import declarative_base


engine_local = create_engine(
    settings.database.database_url,
    echo=settings.database.echo,
    pool_size=int(settings.database.pool_size),
    max_overflow=int(settings.database.max_overflow),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_local,
)

Base = declarative_base()
