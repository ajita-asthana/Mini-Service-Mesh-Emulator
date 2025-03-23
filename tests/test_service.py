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


def test_basic():
    assert 1 == 1
