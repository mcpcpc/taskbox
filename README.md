# TaskBOX

A minimal task manager for automated test.

## Commands

Database initialization.

    flask --app taskbox init-db

## Install

When using git, clone the repository and make it your PWD.

    git clone http://github.com/mcpcpc/taskbox
    cd taskbox/

Create a virtualenv and activate it.

    python3 -m venv venv
    souce venv/bin/activate

Install TaskBOX to the virtual environment.

    pip install -e .

## Deployment

WSGI via waitress.

    pip install waitress
    waitress-serve --call 'taskbox:create_app'
