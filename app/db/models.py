from sqlalchemy import Column, Integer, String, ForeignKey
from .db import Base

class Authors(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    birth_year = Column(Integer)
    nationality = Column(String(64))

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128))
    author_id = Column(Integer, ForeignKey('authors.id'))
    published_year = Column(Integer)
    isbn = Column(String(13))
    pages = Column(Integer)