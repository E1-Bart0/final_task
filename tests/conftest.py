import configparser
import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

sys.path.append(
    os.path.join(os.path.normpath(os.path.dirname(os.path.dirname(__file__))), "src")
)

from db import models  # noqa: E402


@pytest.fixture(scope="session")
def connection():
    config = configparser.ConfigParser()
    config.read("config.ini")
    if "test_database" in config:
        db_name = config["test_database"].get("test_db_name", "test")
        db_user = config["test_database"].get("test_db_user", "test")
        db_password = config["test_database"].get("test_db_password", "test")
        db_port = config["test_database"].get("test_db_port", "65432")
        db_host = config["test_database"].get("test_db_host", "127.0.0.1")
        db_type = config["test_database"].get("test_db_type", "postgresql")
        url = f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        url = "postgresql://test:test@127.0.0.1:65432/test"

    engine = create_engine(url)
    return engine.connect()


@pytest.fixture(scope="session")
def _setup_database(connection):
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()
    yield
    models.Base.metadata.drop_all()


@pytest.fixture()
def db_session(_setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()
