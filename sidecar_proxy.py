# Data plane -> side car proxies that handle communication between services

'''
    - Create a proxy that forwards requests between services.
    - Add features: 
        - Routing: Forward requests based on control plane rules.
        - Logging: Log all requests and responses.
'''

import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

try:
    import requests
except ImportError:
    logging.error("Failed to import 'requests' library. Please install it using 'pip install requests'.")

# Initialize Logging
logging.basicConfig(
    filename='sidecar_proxy.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SidecarProxy(BaseHTTPRequestHandler):
    # Simulated Routing Table
    routing_table = {
        '/service1': 'http://localhost:8001',
        '/service2': 'http://localhost:8002',
    }

    def get_target_service(self, path):
        # Find the target service based on the routing table
        for route, service in self.routing_table.items():
            if path.startswith(route):
                return service
        return None

    def forward_request(self, target_service, path):
        try:
            # Forward the GET request to the target service
            return requests.get(f"{target_service}{path}")
        except requests.exceptions.RequestException as e:
            # Log the error and return a 503 response
            logging.error(f"Error forwarding request to {target_service}{path}: {e}")
            self.send_error(503, f"Service unavailable: {e}")

    def do_GET(self):
        # Log the incoming request
        logging.info(f"Incoming request: {self.path}")

        #Detemine the target service from the routing table
        target_service = self.get_target_service(self.path) 

        if target_service:
            # Forward the request to the appropriate service
            response = self.forward_request(target_service, self.path)

            # Log the forwarded request and response status
            logging.info(f"Forwarded to: {target_service}{self.path} | Response status: {response.status_code}")

            # Send the response back to the client
            self.send_response(response.status_code)
            for header, value in response.headers.items():
                if header not in ('Content-Length', 'Transfer-Encoding', 'Connection'):
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(response.content)
        else:
            # Log the error for unmatched routes
            logging.error(f"No route found for: {self.path}")
            self.send_error(404, f"No route found for: {self.path}")

if __name__ == "__main__":
    # Start the sidecar proxy
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, SidecarProxy)
    logging.info("Sidecar Proxy running on port 8080...")
    httpd.serve_forever()