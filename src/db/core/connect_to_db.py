import configparser
import logging
import os
from contextlib import contextmanager

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

dotenv.load_dotenv()
logging_level = os.getenv("LOGGING_LEVEL")
logging.basicConfig(format="[%(message)s]", level=logging_level)


def get_url_to_db():
    config = configparser.ConfigParser()
    config.read("config.ini")
    if "database" in config:
        db_name = config["database"].get("DB_NAME", "library_db")
        db_user = config["database"].get("DB_USER", "librarian")
        db_password = config["database"].get("DB_PASSWORD", "librarian_password")
        db_port = config["database"].get("DB_PORT", "54321")
        db_host = config["database"].get("DB_HOST", "127.0.0.1")
        db_type = config["database"].get("DB_TYPE", "postgresql")
        return f"{db_type}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return "postgresql://librarian:librarian_password@127.0.0.1:5432/library_db"


engine = create_engine(get_url_to_db())
Base = declarative_base()

Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
