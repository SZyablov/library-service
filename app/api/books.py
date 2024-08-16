from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_

from db.db import get_db
from db.models import Books
from db.schemas import BookCreate, Search

router = APIRouter()

# =======================
# GET
# =======================

# Get all books
# GET /books/
@router.get('')
async def get_books(db: Session = Depends(get_db)):
    return db.query(Books).all()

# Get book by id
# GET /books/{id}/
@router.get('/{id}')
async def get_book_by_id(id, db: Session = Depends(get_db)):
    book = db.query(Books).filter(Books.id == id).first()

    if not book:
        return JSONResponse(status_code=404, content={'status': 404, 'message': 'Book not found!'})
    
    return book

# Search books
# GET /books/search/
@router.get('/search/')
async def search_book(
    title = str | None, 
    author_id = int | None, 
    published_year = int | None, 
    db: Session = Depends(get_db)):

    params = []
    if title != str | None:
        params.append(Books.title.like(title))
    if author_id != int | None:
        params.append(Books.author_id.like(author_id))
    if published_year != int | None:
        params.append(Books.published_year.like(published_year))

    return db.query(Books).filter(and_(*params)).all()

# =======================
# POST
# =======================

# Create a new book
# POST /books/
@router.post('')
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    book = Books(**book.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# =======================
# PUT
# =======================

# Update book by id
# PUT /books/{id}/
@router.put('/{id}')
async def update_book(id, book_body = Body(), db: Session = Depends(get_db)):
    book = db.query(Books).filter(Books.id == id).first()

    if not book:
        return JSONResponse(
            status_code=404,
            content={'status': 404, 'message': 'Books not found!'}
            )
    
    for key, value in book_body.items():
        match(key):
            case 'title':
                book.title = value
            case 'author_id':
                book.author_id = value
            case 'published_year':
                book.published_year = value
            case 'isbn':
                book.isbn = value
            case 'pages':
                book.pages = value
            case _:
                JSONResponse(
                    status_code=400, 
                    content={'status': 400, 'message': 'Error in request body!'}
                    )

    db.commit()
    db.refresh(book)
    return book

# =======================
# DELETE
# =======================

# Delete book by id
# DELETE /books/{id}/
@router.delete('/{id}')
async def delete_book(id: int, db: Session = Depends(get_db)):
    book = db.query(Books).filter(Books.id == id).first()

    if not book:
        return JSONResponse(
            status_code=404,
            content={'status': 404, 'message': 'Books not found!'}
            )
    
    db.delete(book)
    db.commit()
    return book