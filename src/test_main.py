from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books/",
        json={
            "title": "New Book Title",  # Provide a valid title
        },
    )  # END of json
    assert response.status_code == 200
    assert isinstance(
        response.json(), dict
    )  # Changed list to dict based on expected response


def test_delete_book():
    # Create a book to delete
    post_response = client.post(
        "/books/", json={"title": "To Delete", "author": "Someone", "rating": 3.0}
    )  # END of json
    response = client.get("/books/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  # Changed to check for list
    assert data[0]["title"] == "Test Driven Development"  # Accessing first book in list
    assert 0.0 <= data[0]["rating"] <= 5.0
    assert "id" in data[0]

    assert data["title"] == "Test Driven Development"
    assert 0.0 <= data["rating"] <= 5.0
    assert "id" in data
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_book():
    # Create a book to delete
    post_response = client.post(
        "/books/", json={"title": "To Delete", "author": "Someone", "rating": 3.0}
    )

    book_id = post_response.json()["id"]

    # Delete the book
    del_response = client.delete(f"/books/{book_id}")
    assert del_response.status_code == 200
    assert del_response.json() == {"message": "Deleted"}
