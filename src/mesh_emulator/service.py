from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("server.log"), logging.StreamHandler()],
)


class SimpleHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info(
            "%s - - [%s] %s\n"
            % (self.client_address[0], self.log_date_time_string(), format % args)
        )

    # Handle GET methods
    def do_GET(self):
        logging.info(f"Received GET request on path: {self.path}")
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Service is running on the server!", "status": "OK"}
            self.wfile.write(json.dumps(response).encode())
            logging.info("Responded with service status")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found")
            logging.warning(f"GET request to unknown endpoint: {self.path}")

    # Handle Post Requests
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        logging.info(f"Received POST request with body: {body}")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Data received!", "data": data}
            self.wfile.write(json.dumps(response).encode())
            logging.error("Invalid JSON received in POST request")
            return

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Data received!", "data": data}
        self.wfile.write(json.dumps(response).encode())
        logging.info("POST request processed successfully")

    # Handle PUT Requests
    def do_PUT(self):
        content_length = int(self.headers.get("Content-Length", 0))
        logging.info("Received PUT request")
        if content_length == 0:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Empty request body"}
            self.wfile.write(json.dumps(response).encode())
            logging.warning("PUT request with empty body")
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
            logging.error("Invalid JSON format in PUT request")
            return
        if "name" not in data or "status" not in data:
            self.send_response(422)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"error": "Missing required fields"}
            self.wfile.write(json.dumps(response).encode())
            logging.warning("PUT request missing required fields")
            return

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Data Updated!", "data": data}
        self.wfile.write(json.dumps(response).encode())
        logging.info("PUT request processed successfully")

    # Handle Delete Requests
    def do_DELETE(self):
        logging.info("Received DELETE request")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"message": "Resource deleted!"}
        self.wfile.write(json.dumps(response).encode())
        logging.info("DELETE request processed successfully")

    def run_server(self, port=8000):
        host = "localhost"
        server = HTTPServer((host, port), SimpleHandler)
        print(f"Service running on {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    handler = SimpleHandler
    server = HTTPServer(("localhost", 8001), handler)
    logging.info("Starting server on port 8001...")

# Testing the Service
# GET:  curl http://localhost:8001/status
# POST: curl -X POST http://localhost:8001 -H "Content-Type: application/json" -d '{"name": "example"}'
# PUT: curl -X PUT http://localhost:8001 -H "Content-Type: application/json" -d '{"name": "updated example"}'
# DELETE: curl -X DELETE http://localhost:8001
