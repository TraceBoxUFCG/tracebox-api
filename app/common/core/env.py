from prettyconf import config
from sqlalchemy.engine.url import URL

SQLALCHEMY_DRIVER_NAME = config(
    "SQLALCHEMY_DRIVER_NAME",
    default="postgresql",
)
SQLALCHEMY_HOST = config(
    "SQLALCHEMY_HOST",
    default="localhost",
)
SQLALCHEMY_USERNAME = config(
    "SQLALCHEMY_USERNAME",
    default="postgres",
)
SQLALCHEMY_PASSWORD = config(
    "SQLALCHEMY_PASSWORD",
    default="postgres",
)
SQLALCHEMY_DATABASE = config(
    "SQLALCHEMY_DATABASE",
    default="tracebox_test",
)
SQLALCHEMY_PORT = config(
    "SQLALCHEMY_PORT",
    default="5432",
)
SQLALCHEMY_DATABASE_URL = config(
    "SQLALCHEMY_DATABASE_URL",
    default=None,
)

ECHO_QUERIES = config("ECHO_QUERIES", default=False, cast=config.boolean)


if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = str(
        URL.create(
            drivername=SQLALCHEMY_DRIVER_NAME,
            username=SQLALCHEMY_USERNAME,
            password=SQLALCHEMY_PASSWORD,
            host=SQLALCHEMY_HOST,
            port=SQLALCHEMY_PORT,
            database=SQLALCHEMY_DATABASE,
        )
    )

MAX_OVERFLOW = config("MAX_OVERFLOW", default=40)
POOL_SIZE = config("POOL_SIZE", default=30)
