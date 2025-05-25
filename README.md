# Mini-Service-Mesh-Emulator
![pytest](https://github.com/ajita-asthana/Mini-Service-Mesh-Emulator/actions/workflows/pytest.yml/badge.svg)

Build a simple simulation of a service mesh to manage communication between microservices.

# Features
  * Simulate microservices as Python processes or threads
  * Include a basic control plane for managing routing rules
  * Implement load balancing and service discovery


# SignUp

curl -X POST http://localhost:8000/signup \
-H "Content-Type: application/json" \
-d '{"username": "alice", "password": "123"}'

# Create Order 

curl -X POST http://localhost:8000/order \
-H "Content-Type: application/json" \
-d '{"user_id": "alice", "product_id": "book", "quantity": 2}'