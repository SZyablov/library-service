from fastapi import FastAPI
from fastapi.responses import FileResponse
from api import (authors, books)
from contextlib import asynccontextmanager
from db.db import engine, Base



app = FastAPI()
 
app.include_router(books.router,   prefix='/books')
app.include_router(authors.router, prefix='/authors')

# Main page with book and author forms
@app.get('/')
async def root():
    return FileResponse("public/index.html")

# Main page with book and author forms
@app.get('/books_search')
async def books_search():
    return FileResponse("public/search.html")

#
# Lifespan
#

main_app_lifespan = app.router.lifespan_context

@asynccontextmanager
async def lifespan_wrapper(app):

    # execute code on startup
    print('Connecting to the database...')
    Base.metadata.create_all(bind=engine)
    print('Connected to the database')

    async with main_app_lifespan(app) as maybe_state:
        yield maybe_state
    # execute code on shutdown

app.router.lifespan_context = lifespan_wrapper