## Development instructions


### SetUp

```bash
# create a virtualenv
$ python3.12 -m venv .venv

# activate the virtualenv
$ source .venv/bin/activate

# deactivate the virtualenv
$ deactivate
```

### Testing with pytest

```bash
$ source .venv/bin/activate
$ pip install pytest
$ pytest
```

### How to rebase
  * Switch to the main branch
  * Run git fetch/ git pull
  * Go to your issue_branch
  * Run git rebase origin/main
  * resolve merge conflicts if any 
  * Run git push -f