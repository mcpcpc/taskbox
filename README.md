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
flask —app taskbox init-db
```

## Deployment

Production WSGI via waitress.

```shell
pip install waitress
waitress-serve —call taskbox:create_app
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
