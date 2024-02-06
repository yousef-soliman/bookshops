from fastapi.testclient import TestClient
from app.database.test_db import override_get_db
from app.main import app
from app.database.db import get_db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_author():
    response = client.post(
        "/authors", json={"name": "Test Author", "birth_date": "2000-01-01"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Author"
    assert data["birth_date"] == "2000-01-01"


def test_create_author_same_name_same_birth_date():
    response = client.post(
        "/authors", json={"name": "Test Author", "birth_date": "2005-01-01"}
    )
    assert response.status_code == 201
    response = client.post(
        "/authors", json={"name": "Test Author", "birth_date": "2005-01-01"}
    )
    assert response.status_code == 400


def test_create_author_same_name_different_birth_date():
    response = client.post(
        "/authors", json={"name": "Test Author", "birth_date": "2004-01-01"}
    )
    assert response.status_code == 201
    response = client.post(
        "/authors", json={"name": "Test Author", "birth_date": "2001-01-01"}
    )
    assert response.status_code == 201


def test_get_all_authors():
    response = client.get("/authors")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_author():
    response = client.get("/authors/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "birth_date" in data


def test_get_author_not_found():
    response = client.get("/authors/9999")
    assert response.status_code == 404
    assert "detail" in response.json()
    assert response.json()["detail"] == "Author not found"
