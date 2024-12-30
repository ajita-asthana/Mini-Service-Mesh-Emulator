from http.server import BaseHTTPRequestHandler, HTTPServer

class MockService2(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"message": "Hello from Service 2!"}')

if __name__ == "__main__":
    server = HTTPServer(('localhost', 8002), MockService2)
    print("Service 2 running on port 8002....")
    server.serve_forever()