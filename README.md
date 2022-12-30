# TaskBOX

A minimal task manager for automated test.

## Commands

Database initialization

    flask --app taskbox init-db

 ## Install

Create a virtualenv and activate it::

    python3 -m venv venv
    souce venv/bin/activate

Install TaskBOX

    pip install -e .

## Deployment

WSGI via waitress

    pip install waitress
    waitress-serve --call 'taskbox:create_app'
