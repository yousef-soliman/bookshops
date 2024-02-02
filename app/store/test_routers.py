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


def test_update_store_add():
    author = Author(
        name="Test Author", birth_date=datetime.strptime("2019-01-01", "%Y-%m-%d")
    )
    db.add(author)
    db.commit()

    book = Book(title="Test Book", publish_year=2019, barcode="123456", author=author)
    db.add(book)
    db.commit()

    store_payload = {"barcode": "123456", "quantity": 10}

    response = client.post("/store/leftover/add", json=store_payload)

    assert response.status_code == 200

    data = response.json()
    assert data["quantity"] == 10


def test_update_store_remove():
    store_payload = {"barcode": "123456", "quantity": 10}

    response = client.post("/store/leftover/remove", json=store_payload)

    assert response.status_code == 200

    data = response.json()
    assert data["quantity"] == 10
