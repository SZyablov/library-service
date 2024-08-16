from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.db import get_db
from db.models import Authors
from db.schemas import AuthorCreate

router = APIRouter()

# =======================
# GET
# =======================

# Get all authors
# GET /authors/
@router.get('')
async def get_authors(db: Session = Depends(get_db)):
    return db.query(Authors).all()

# Get author by id
# GET /authors/{id}/
@router.get('/{id}')
async def get_author_by_id(id, db: Session = Depends(get_db)):
    author = db.query(Authors).filter(Authors.id == id).first()

    if not author:
        return JSONResponse(status_code=404, content={'status': 404, 'message': 'Author not found!'})
    
    return author

# =======================
# POST
# =======================

# Create a new author
# POST /authors/
@router.post('')
async def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    author = Authors(**author.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

# =======================
# PUT
# =======================

# Update author by id
# PUT /authors/{id}/
@router.put('/{id}')
async def update_author(id, author_body = Body(), db: Session = Depends(get_db)):
    author = db.query(Authors).filter(Authors.id == id).first()

    if not author:
        return JSONResponse(
            status_code=404,
            content={'status': 404, 'message': 'Author not found!'}
            )
    
    for key, value in author_body.items():
        match(key):
            case 'name':
                author.name = value
            case 'birth_year':
                author.birth_year = value
            case 'nationality':
                author.nationality = value
            case _:
                JSONResponse(
                    status_code=400, 
                    content={'status': 400, 'message': 'Error in request body!'}
                    )

    db.commit()
    db.refresh(author)
    return author

# =======================
# DELETE
# =======================

# Delete author by id
# DELETE /authors/{id}/
@router.delete('/{id}')
async def delete_author(id: int, db: Session = Depends(get_db)):
    author = db.query(Authors).filter(Authors.id == id).first()

    if not author:
        return JSONResponse(
            status_code=404,
            content={'status': 404, 'message': 'Authors not found!'}
            )
    
    db.delete(author)
    db.commit()
    return author