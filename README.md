# Mini-Service-Mesh-Emulator
![pytest](https://github.com/ajita-asthana/Mini-Service-Mesh-Emulator/actions/workflows/pytest.yml/badge.svg)
![Build Status](https://github.com/your-username/your-repo/actions/workflows/ci.yml/badge.svg)


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

# How to rebase 
  * Switch to the main branch
  * Run git fetch/ git pull
  * Go to your issue_branch
  * Run git rebase origin/main
  * resolve merge conflicts if any 
  * Run git push -f