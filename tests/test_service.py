import threading
import time
from http.server import HTTPServer

import pytest
import requests

from mesh_emulator import service

HOST = "localhost"
PORT = 8000


def run_server():
    httpd = HTTPServer((HOST, PORT), service.SimpleHandler)
    httpd.serve_forever()


@pytest.fixture(scope="module", autouse=True)
def start_server():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)  # Give a server a second to start
    yield


def test_status_endpoint():
    response = requests.get(f"http://{HOST}:{PORT}/status")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Service is running on the server!"
    assert data["status"] == "OK"


def test_not_found_endpoint():
    response = requests.get(f"http://{HOST}:{PORT}/invalid")
    assert response.status_code == 404
    assert response.text == "Endpoint not found"


# ** Happy Path - Valid Requests **
def test_do_put():
    """
    Tests the PUT request handling.
    """
    url = f"http://localhost:{PORT}"
    test_data = {"name": "Task1", "status": "completed"}

    response = requests.put(url, json=test_data)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["message"] == "Data Updated!"
    assert response_json["data"] == test_data


# ** Sad Path - Empty Request Body **
def test_put_empty_body():
    """
    Tests a PUT request with an empty body
    """
    url = f"http://localhost:{PORT}"

    response = requests.put(url, data="")  # No JSON body

    assert response.status_code == 400
    assert response.json()["error"] == "Empty request body"


# Sad Path - Invalid JSON format
def test_put_invalid_json():
    """
    Tests a PUT request with invalid JSON format
    """
    url = f"http://localhost:{PORT}"
    invalid_json = "{'name': 'Task1', 'status': 'completed'}"  # Incorrect JSON format
    response = requests.put(
        url, data=invalid_json, headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 400
    assert response.json()["error"] == "Invalid JSON data"


def test_put_missing_fields():
    """
    Tests a PUT request with missing required fields.
    """
    url = f"http://localhost:{PORT}"

    incomplete_data = {"name": "Task1"}  # Missing "status"

    response = requests.put(url, json=incomplete_data)
    assert response.status_code == 422
    assert response.json()["error"] == "Missing required fields"


def test_basic():
    assert 1 == 1
