from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    response = client.post("/books/", 
        json= {
            "title": "Test Driven Developement",
            "author": "Kent Beck", 
            "rating": 4.5 
        }
        assert response.status_code == 200
        data = response.json() 
        assert data["title"] == "Test Driven Development"
        assert 0.0 <= data["rating"] <= 5.0 
        assert "id" in data 

def test_list_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_book():
    # Create a book to delete
    post_response = client.post("/books/", 
                json = {
                    "title": "To Delete",
                    "author": "Someone",
                    "rating": 3.0 
                })

    book_id = post_response.json()["id"]

    # Delete the book 
    del_response = client.delete(f"/books/{book_id}")
    assert del_response.status_code == 200
    assert del_response.json() == {"message": "Deleted"}

    