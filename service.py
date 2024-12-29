from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleService(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello from Service!")

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8001), SimpleService)
    print("Service running on port 8001")
    server.serve_forever()