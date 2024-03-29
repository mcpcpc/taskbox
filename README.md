# TaskBOX

A minimal task manager for automated test.

## Install

### PyPI

Install and update using`pip:

```shell
pip install -U taskbox
```

### Repository

When using git, clone the repository and change your PWD.

```shell
git clone http://github.com/mcpcpc/taskbox
cd taskbox/
```

Create and activate a virtual environment.

```shell
python3 -m venv venv
source venv/bin/activate
```

Install TaskBOX to the virtual environment.

```shell
pip install -e .
```

## Commands

### db-init

The Sqlite3 database can be initialized or re-initialized with the
following command.

```shell
flask --app taskbox init-db
```

## Deployment

Before deployment, we *strongly* encourage you to override the
default `SECRET_KEY` variable. This can be done by creating a
`conf.py` file and placing it in the same root as the instance (i.e. typically where the SQLite database resides).

```python
SECRET_KEY = “192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf“
```

There are a number of ways to generate a secret key value. The
simplest would be to use the built-in secrets Python library.

```shell
$ python -c ‘import secrets; print(secrets.token_hex())’
‘192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf’
```

### Waitress

Production WSGI via waitress.

```shell
pip install waitress
waitress-serve --call taskbox:create_app
```

## Test

```shell
python3 -m unittest
```

Run with coverage report.

```shell
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index.html in a browser
```
