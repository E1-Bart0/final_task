from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from src.db.core.connect_to_db import Base


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(60), index=True, unique=True, nullable=False)
    book = relationship("Book", backref="book", passive_deletes=True)


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=True, index=True)
    author_id = Column(
        Integer, ForeignKey("author.id", ondelete="CASCADE"), nullable=True
    )

    # unique constraints across multiple columns and Indexing by name, year, author
    __table_args__ = (
        UniqueConstraint(
            "name",
            "year",
            "author_id",
            name="_books_uc",
            deferrable=True,
            initially="DEFERRED",
        ),
        Index("_book_index", "name", "year", "author_id"),
    )
