import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class SimpleHandler(BaseHTTPRequestHandler):
    # Handle GET methods
    def do_GET(self):
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Service is running on the server!", "status": "OK"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found")

    # Handle Post Requests
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        data = json.loads(body)

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Data received!", "data": data}
        self.wfile.write(json.dumps(response).encode())

    # Handle PUT Requests
    def do_PUT(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Empty request body"}
            self.wfile.write(json.dumps(response).encode())
            return

        body = self.rfile.read(content_length).decode()
        try:
            data = json.loads(body)
            if not isinstance(data, dict):
                raise ValueError("Invalid JSON format")
        except (json.JSONDecodeError, ValueError):
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Invalid JSON data"}
            self.wfile.write(json.dumps(response).encode())
            return
        if "name" not in data or "status" not in data:
            self.send_response(422)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Missing required fields"}
            self.wfile.write(json.dumps(response).encode())
            return

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Data Updated!", "data": data}
        self.wfile.write(json.dumps(response).encode())

    # Handle Delete Requests
    def do_DELETE(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Resource deleted!"}
        self.wfile.write(json.dumps(response).encode())


if __name__ == "__main__":
    host = "localhost"
    port = 8000
    server = HTTPServer((host, port), SimpleHandler)
    print(f"Service running on {host}:{port}")
    server.serve_forever()

# Testing the Service
# GET:  curl http://localhost:8001/status
# POST: curl -X POST http://localhost:8001 -H "Content-Type: application/json" -d '{"name": "example"}'
# PUT: curl -X PUT http://localhost:8001 -H "Content-Type: application/json" -d '{"name": "updated example"}'
# DELETE: curl -X DELETE http://localhost:8001
