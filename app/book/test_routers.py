from datetime import datetime
from fastapi.testclient import TestClient
from app.author.models import Author
from app.book.models import Book
from app.database.test_db import TestingSessionLocal, override_get_db
from app.main import app
from app.database.db import get_db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

db = TestingSessionLocal()


def test_create_book():
    author = Author(
        name="Test Author", birth_date=datetime.strptime("2009-01-01", "%Y-%m-%d")
    )
    db.add(author)
    db.commit()

    book_payload = {
        "title": "Test Book",
        "publish_year": "1995",
        "barcode": "123456",
        "author": author.id,
    }

    response = client.post("/books/", json=book_payload)

    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Book"
    assert data["publish_year"] == 1995
    assert data["barcode"] == "123456"
    assert "author" in data
    assert data["author"]["id"] == author.id


def test_create_book_with_same_title_same_publish_year():
    author = Author(
        name="Test Author", birth_date=datetime.strptime("2007-01-01", "%Y-%m-%d")
    )
    db.add(author)
    db.commit()

    book_payload = {
        "title": "Test Book",
        "publish_year": "2006",
        "barcode": "123456",
        "author": author.id,
    }

    response = client.post("/books/", json=book_payload)

    assert response.status_code == 200

    book_payload = {
        "title": "Test Book",
        "publish_year": "2006",
        "barcode": "123456",
        "author": author.id,
    }

    response = client.post("/books/", json=book_payload)

    assert response.status_code == 400


def test_create_book_with_same_title_different_publish_year():
    author = Author(
        name="Test Author", birth_date=datetime.strptime("2017-01-01", "%Y-%m-%d")
    )
    db.add(author)
    db.commit()

    book_payload = {
        "title": "Test Book",
        "publish_year": "2007",
        "barcode": "123456",
        "author": author.id,
    }

    response = client.post("/books/", json=book_payload)

    assert response.status_code == 200

    book_payload = {
        "title": "Test Book",
        "publish_year": "2008",
        "barcode": "123456",
        "author": author.id,
    }

    response = client.post("/books/", json=book_payload)

    assert response.status_code == 200


def test_get_all_books():
    response = client.get("/books/")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)


def test_get_book():
    test_book = Book(
        title="Test Book",
        publish_year="2022",
        barcode="123456",
        author_id=1,
    )
    db.add(test_book)
    db.commit()

    response = client.get(f"/books/{test_book.id}")

    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Book"
    assert data["publish_year"] == 2022
    assert data["barcode"] == "123456"
    assert "author" in data
    assert data["author"]["id"] == test_book.author_id
