# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
import pdb
from models import (
    SessionLocal,
    Book,
    Author,
    Client,
    BookClientRelationship,
    BookInDB,
    AuthorInDB,
    Client as ClientModel,
    BookClientRelationshipInDB,
    BookCreate,
    AuthorCreate,
)

app = FastAPI()

# OAuth2 Bearer Token for authentication
oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token", authorizationUrl="https://github.com/login/oauth/authorize")

# Dependency to get the current database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Your FastAPI routes go here
# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"}
# Add a book
pdb.set_trace()

@app.post("/books/", response_model=BookInDB)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        # Your book creation logic here
        print("Request Payload:", book.dict())

        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        print("message Book added successfully")
        return db_book
        
    except Exception as e:
        # Log the exception
        print("Exception:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    

# Edit the book's title and author
@app.put("/books/{book_id}", response_model=BookInDB)
def edit_book(book_id: int, title: str, author_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.title = title
        book.author_id = author_id
        db.commit()
        db.refresh(book)
        return book
    raise HTTPException(status_code=404, detail="Book not found")

# Retrieve a list of books with filtering options
@app.get("/books/filter/")
def filter_books(title_starts_with: str = "", author_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if title_starts_with:
        query = query.filter(Book.title.startswith(title_starts_with))
    if author_id:
        query = query.filter(Book.author_id == author_id)
    books = query.all()
    return books

# Add multiple books by the same author
@app.post("/authors/{author_id}/books/", response_model=list[BookInDB])
def add_books_by_author(author_id: int, books: list[BookCreate], db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if author:
        for book in books:
            book.author_id = author_id
            db_book = Book(**book.dict())
            db.add(db_book)
        db.commit()
        return books
    raise HTTPException(status_code=404, detail="Author not found")

# Add an author
@app.post("/authors/", response_model=AuthorInDB)
def add_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

# Create a client
@app.post("/clients/", response_model=ClientModel)
def create_client(client: ClientModel, db: Session = Depends(get_db)):
    db_client = ClientModel(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Retrieve a list of books borrowed by the client
@app.get("/clients/{client_id}/books/", response_model=list[BookClientRelationshipInDB])
def get_books_borrowed_by_client(client_id: int, db: Session = Depends(get_db)):
    client_books = db.query(BookClientRelationship).filter(BookClientRelationship.client_id == client_id).all()
    return client_books

# Link a client to a book (client borrowed the book)
@app.post("/clients/{client_id}/books/{book_id}/link/", response_model=BookClientRelationshipInDB)
def link_client_to_book(client_id: int, book_id: int, db: Session = Depends(get_db)):
    relationship = BookClientRelationship(client_id=client_id, book_id=book_id)
    db.add(relationship)
    db.commit()
    db.refresh(relationship)
    return relationship

# Unlink a client from a book (client returned the book)
@app.post("/clients/{client_id}/books/{book_id}/unlink/")
def unlink_client_from_book(client_id: int, book_id: int, db: Session = Depends(get_db)):
    relationship = db.query(BookClientRelationship).filter(
        (BookClientRelationship.client_id == client_id) & (BookClientRelationship.book_id == book_id)
    ).first()
    if relationship:
        db.delete(relationship)
        db.commit()
        return {"detail": "Book unlinked from client"}
    raise HTTPException(status_code=404, detail="Relationship not found")
