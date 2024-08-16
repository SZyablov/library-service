from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.db import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db



client = TestClient(app)

#
# Test if we can post
# =========================================================== POST /books/
def test_post_book():
    response = client.post(
        "/books/",
        json={
            "title":"Book",
            "author_id":1,
            "isbn":"random",
            "published_year":2024,
            "pages":42
            }
    )
    assert response.status_code == 200, response.text
    data=response.json()
    assert data['id'] == 1
    assert data['published_year'] == 2024
    assert data['title'] == 'Book'
# ========================================================= POST /authors/
def test_post_author():
    response = client.post(
        "/authors/",
        json={
            "name":"Author",
            "nationality":"Earth",
            "birth_year":1987
            }
    )
    assert response.status_code == 200, response.text
    data=response.json()
    assert data['id'] == 1
    assert data['name'] == "Author"
    assert data['birth_year'] == 1987
# ==================================================================== END



#
# Test if we can get
# ============================================================ GET /books/
def test_get_books():
    response = client.get(
        "/books/",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]['id'] == 1
# ===================================================== GET /books/search/
def test_book_search():
    # check all args
    response = client.get(
        "/books/search/?title=Book&author_id=1&published_year=2024",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]['id'] == 1
    
    # check 2 args out of 3
    response = client.get(
        "/books/search/?title=Book&published_year=2024",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]['id'] == 1

    # check a situation in which books are known to be impossible to find
    response = client.get(
        "/books/search/?title=kooB",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 0
# ========================================================== GET /authors/
def test_get_authors():
    response = client.get(
        "/authors/",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]['id'] == 1
# ==================================================================== END



#
# Test if we can get by id
# ======================================================== GET /books/{id}
def test_get_book_by_id():
    response = client.get(
        "/books/1",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == 1
# ===================================== GET /authors/{id}
def test_get_author_by_id():
    response = client.get(
        "/authors/1",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['id'] == 1
# =================================================================== END



#
# Test if we can put
# ======================================================== PUT /books/{id}
def test_put_book():
    # check book
    response = client.get(
        "/books/1"
    )
    data=response.json()
    assert data['id'] == 1
    assert data['title'] == "Book"
    assert data['isbn'] == 'random'

    # change it
    response = client.put(
        "/books/1",
        json={
            "title":"Book renamed",
            "isbn":"RANDOM"
            }
    )
    assert response.status_code == 200, response.text
    data=response.json()
    assert data['id'] == 1

    # re-check book
    response = client.get(
        "/books/1"
    )
    data=response.json()
    assert data['id'] == 1
    assert data['title'] == "Book renamed"
    assert data['isbn'] == 'RANDOM'
# ====================================================== PUT /authors/{id}
def test_put_author():
    # check author
    response = client.get(
        "/authors/1"
    )
    data=response.json()
    assert data['id'] == 1
    assert data['nationality'] == "Earth"

    # change them
    response = client.put(
        "/authors/1",
        json={
            "nationality":"Mars"
            }
    )
    assert response.status_code == 200, response.text
    data=response.json()
    assert data['id'] == 1

    # re-check author
    response = client.get(
        "/authors/1"
    )
    data=response.json()
    assert data['id'] == 1
    assert data['nationality'] == "Mars"
# ==================================================================== END



#
# Test if we can delete
# ===================================================== DELETE /books/{id}
def test_delete_book():
    response = client.delete(
        "/books/1"
    )
    assert response.status_code == 200, response.text
    
    response = client.get(
        "/books/"
    )
    assert response.status_code == 200, response.text
    data=response.json()
    assert data == []
# =================================================== DELETE /authors/{id}
def test_delete_author():
    response = client.delete(
        "/authors/1"
    )
    assert response.status_code == 200, response.text
    
    response = client.get(
        "/authors/"
    )
    assert response.status_code == 200, response.text
    data=response.json()
    assert data == []
# ==================================================================== END