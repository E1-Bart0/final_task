from typing import Optional

from sqlalchemy import Column, ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from .core.connect_to_db import Base


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)
    book = relationship("Book", backref="author", passive_deletes=True)

    # unique constraints across multiple columns and Indexing by name, year, author
    __table_args__ = (
        UniqueConstraint(
            "first_name",
            "last_name",
        ),
        Index("_author_index", "first_name", "last_name"),
    )

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @hybrid_property
    def as_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    def __repr__(self):
        return str(self.as_dict)


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    year = Column(Integer, nullable=True, index=True)
    author_id = Column(
        Integer,
        ForeignKey("author.id", ondelete="CASCADE"),
        nullable=True,
        default=None,
    )

    # unique constraints across multiple columns and Indexing by name, year, author
    __table_args__ = (
        UniqueConstraint(
            "name",
            "year",
            "author_id",
        ),
        Index("_book_index", "name", "year", "author_id"),
    )

    def __init__(self, name: str, year: Optional[int], author_id: Optional[int]):
        self.name = name
        self.year = year
        self.author_id = author_id

    @hybrid_property
    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "year": self.year,
            "author": self.author.as_dict if self.author_id else None,
        }

    def __repr__(self):
        return str(self.as_dict)
