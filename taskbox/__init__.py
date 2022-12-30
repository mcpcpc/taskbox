#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import getenv

from flask import Flask

from taskbox.db import init_app
from taskbox.api import tasks
from taskbox.ux import home


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=getenv("DB_PATH", "/tmp/taskbox.sqlite"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)
    init_app(app)
    app.register_blueprint(tasks)
    app.register_blueprint(home)
    return app
