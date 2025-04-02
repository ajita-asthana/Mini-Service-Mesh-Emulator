# Mini-Service-Mesh-Emulator
![pytest](https://github.com/ajita-asthana/Mini-Service-Mesh-Emulator/actions/workflows/main.yml/badge.svg)

Build a simple simulation of a service mesh to manage communication between microservices.

# Features
  * Simulate microservices as Python processes or threads
  * Include a basic control plane for managing routing rules
  * Implement load balancing and service discovery

# SetUp

```bash
# create a virtualenv
$ python3.12 -m venv .venv

# activate the virtualenv
$ source .venv/bin/activate

# deactivate the virtualenv
$ deactivate
```

## Testing with pytest

```bash
$ source .venv/bin/activate
$ pip install pytest
$ pytest
```