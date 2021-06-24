import configparser
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

config = configparser.ConfigParser()
config.read("config.ini")

DB_NAME = config["database"].get("DATABASE_NAME", "library_db")
DB_USER = config["database"].get("DATABASE_USER", "librarian")
DB_PASSWORD = config["database"].get("DATABASE_PASSWORD", "librarian_password")
DB_PORT = config["database"].get("DATABASE_PORT", "5432")
DB_HOST = config["database"].get("DATABASE_HOST", "127.0.0.1")
DB_TYPE = config["database"].get("DATABASE_TYPE", "postgresql")

URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(URL, echo=True)
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
