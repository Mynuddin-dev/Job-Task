# models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
from pydantic import BaseModel  # Import BaseModel from pydantic

DATABASE_URL = "postgresql://postgres:test1234@localhost:5432/testdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)

class AuthorCreate(BaseModel):  # Pydantic model for creating an Author
    full_name: str

class AuthorInDB(BaseModel):
    id: int
    full_name: str

    class Config:
        orm_mode = True

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship(Author)

class BookCreate(BaseModel):  # Pydantic model for creating a Book
    title: str
    author_id: int

class BookInDB(BaseModel):
    id: int
    title: str
    author_id: int

    class Config:
        from_attributes = True

class Client(BaseModel):
    id: int
    full_name: str

    class Config:
        from_attributes = True

class BookClientRelationship(Base):
    __tablename__ = "book_client_relationship"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    borrowed_date = Column(DateTime, default=datetime.utcnow)
    returned_date = Column(DateTime, nullable=True)

class BookClientRelationshipInDB(BaseModel):
    id: int
    book_id: int
    client_id: int
    borrowed_date: datetime
    returned_date: datetime

    class Config:
        from_attributes = True
