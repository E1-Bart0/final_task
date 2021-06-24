from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.db.core.connect_to_db import Base


class Human(Base):
    __abstract__ = True
    __tablename__ = None

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))


class Student(Human):
    __tablename__ = "student"


class Teacher(Human):
    __tablename__ = "teacher"
    homework_done = relationship("HomeworkResult")


class Homework(Base):
    __tablename__ = "homework"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    created = Column(DateTime, default=datetime.now())
    deadline = Column(Integer)
    homework_result = relationship(
        "HomeworkResult", uselist=False, back_populates="homework"
    )


class HomeworkResult(Base):
    __tablename__ = "homework_result"
    id = Column(Integer, primary_key=True)
    solution = Column(Text)
    author_id = Column(Integer, ForeignKey("student.id", ondelete="CASCADE"))
    author = relationship("Student")
    created = Column(DateTime, default=datetime.now())
    teacher_id = Column(
        Integer, ForeignKey("teacher.id", ondelete="CASCADE"), nullable=True
    )
    homework_id = Column(Integer, ForeignKey("homework.id"))
    homework = relationship("Homework", back_populates="homework_result")
