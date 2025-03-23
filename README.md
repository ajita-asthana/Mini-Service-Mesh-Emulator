# Mini-Service-Mesh-Emulator
Build a simple simulation of a service mesh to manage communication between microservices.

# Features 
  * Simulate microservices as Python processes or threads
  * Include a basic control plane for managing routing rules
  * Implement load balancing and service discovery

# Libraries
  - socket
  - threading
  - json
  - http.server

# Virtual Environment SetUp 
  - To activate: source .venv/bin/activate
  - To deactivate: deactivate
  
## Testing with pytest

```bash
$ source .venv/bin/activate
$ pip install pytest
$ pytest
```