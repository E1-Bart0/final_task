import configparser

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from src.db import models
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture(scope="session")
def connection():
    config = configparser.ConfigParser()
    config.read("config.ini")

    db_name = config["test_database"].get("test_db_name", "test")
    db_user = config["test_database"].get("test_db_user", "test")
    db_password = config["test_database"].get("test_db_password", "test")
    db_port = config["test_database"].get("test_db_port", "65432")
    db_host = config["test_database"].get("test_db_host", "127.0.0.1")
    db_type = config["test_database"].get("test_db_type", "postgresql")

    url = f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(url)
    return engine.connect()


@pytest.fixture(scope="session")
def setup_database(connection):
    models.Base.metadata.bind = connection
    models.Base.metadata.create_all()
    yield
    models.Base.metadata.drop_all()


@pytest.fixture()
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    transaction.rollback()
