## How to contribute to Deer

### First time setup

* Configure git username and email
```
$ git config --global user.name 'your name'
$ git config --global user.email 'your email'
```

* Fork Deer to your Github account by clicking the [Fork](https://github.com/nxf7/deer/fork)
button

* Clone the main Deer repository locally (through https or preferably ssh)
```
$ git clone https://github.com/nxf7/deer
$ cd deer
```

* Add your fork as a remote to push changes to
```
$ git remote add fork https://github.com/{username}/deer
```

* Upgrade pip and setuptools
```
$ python -m pip install --upgrade pip setuptools
```

* Create a virtual environment and activate it
```
$ python3 -m venv env
$ . env/bin/activate
```

* Install Deer and its dependencies in editable mode
```
$ pip install -e .[extra] # this installs dev dependencies too
```

* Install pre-commit hooks
```
$ pre-commit install
```

### Start coding
* Create a branch to identify the issue you would like to work on
```
$ git fetch origin
$ git checkout -b your-branch-name origin/2.0.x
```
* If you're submitting a feature addition or change, branch off of the main branch
```
$ git fetch origin
$ git checkout -b your-branch-name origin/main
```

* Include tests that cover the code changes you made
* Push your commits to your fork on GitHub and submit a pull request
```
$ git push --set-upstream fork your-branch-name
```

### Running the tests
```
$ pytest
```
