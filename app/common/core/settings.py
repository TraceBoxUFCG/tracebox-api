from pydantic import BaseModel

from app.common.core.env import ECHO_QUERIES, MAX_OVERFLOW, POOL_SIZE, SQLALCHEMY_DATABASE, SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DRIVER_NAME, SQLALCHEMY_HOST, SQLALCHEMY_PASSWORD, SQLALCHEMY_PORT, SQLALCHEMY_USERNAME

class DatabaseSettings(BaseModel):
    driver: str = SQLALCHEMY_DRIVER_NAME
    host:str = SQLALCHEMY_HOST
    username: str = SQLALCHEMY_USERNAME
    password: str = SQLALCHEMY_PASSWORD
    database:str = SQLALCHEMY_DATABASE
    port:str = SQLALCHEMY_PORT
    database_url:str  = SQLALCHEMY_DATABASE_URL
    echo: bool = ECHO_QUERIES
    max_overflow: int = MAX_OVERFLOW
    pool_size: int = POOL_SIZE


class Settings(BaseModel):
    database: DatabaseSettings = DatabaseSettings()

settings = Settings()