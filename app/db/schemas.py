from pydantic import BaseModel

#
# Author
#

class AuthorBase(BaseModel):
    name: str
    birth_year: int
    nationality: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True

#
# Book
#

class BookBase(BaseModel):
    title: str 
    author_id: int
    published_year: int
    isbn: str
    pages: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        from_attributes = True

class Search(BaseModel):
    title: str
    author_id: int
    published_year: int