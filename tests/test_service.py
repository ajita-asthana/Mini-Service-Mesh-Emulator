from fastapi.testclient import TestClient

from mesh_emulator.service import app

client = TestClient(app)

HOST = "localhost"
PORT = 8000


def test_status_endpoint():
    response = client.get(f"http://{HOST}:{PORT}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Service is running on the server!"
    assert data["status"] == "OK"


def test_not_found_endpoint():
    response = client.get(f"http://{HOST}:{PORT}/invalid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_do_put():
    """
    Tests the PUT request handling.
    """
    url = f"http://localhost:{PORT}"
    test_data = {"name": "Task1", "status": "completed"}

    response = client.put(url, json=test_data)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["message"] == "Data Updated!"
    assert response_json["data"] == test_data


def test_put_empty_body():
    """
    Tests a PUT request with an empty body
    """
    url = f"http://localhost:{PORT}"

    response = client.put(url, data="")  # No JSON body

    assert response.status_code == 422


def test_put_invalid_json():
    """
    Tests a PUT request with invalid JSON format
    """
    url = f"http://localhost:{PORT}"
    invalid_json = "{'name': 'Task1', 'status': 'completed'}"  # Incorrect JSON format
    response = client.put(
        url, data=invalid_json, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
