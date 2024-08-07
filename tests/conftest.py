from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from app.common.core.settings import settings
import os

import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import create_database, database_exists

from app.main import app

from app.common.dependencies import get_session
from tests.supplier.factories import make_address, make_supplier  # noqa: F401

engine = create_engine(
    settings.database.database_url,
    echo=settings.database.echo,
)
pytest_plugins = ["pytest_asyncio"]


engine = create_engine(settings.database.database_url)


@pytest.fixture()
def session():
    if not engine.url.database.endswith("_test"):
        raise Exception(
            "Dear lord! for your safety only db name ending `_test` is allowed."
        )

    if not database_exists(engine.url):
        create_database(engine.url)

    root_dir = os.getcwd()
    script_location = root_dir + "/migrations"
    alembic_ini = root_dir + "/alembic.ini"
    config = Config(file_=alembic_ini)

    config.set_main_option("script_location", script_location)
    config.set_main_option("sqlalchemy.url", settings.database.database_url)

    # drop everything
    # command.downgrade(config, "base")
    # run migrations
    command.upgrade(config, "head")

    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin()

    # Begin a nested transaction (using SAVEPOINT).
    nested = connection.begin_nested()

    # If the application code calls session.commit, it will end the nested
    # transaction. Need to start a new one when that happens.
    @sa.event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    # Rollback the overall transaction, restoring the state before the test ran.
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    test_client = TestClient(app)
    yield test_client
    del app.dependency_overrides[get_session]
