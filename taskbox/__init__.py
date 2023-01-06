#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from os import makedirs

from flask import Flask

from taskbox.db import init_app
from taskbox.devices import devices
from taskbox.runner import runner
from taskbox.tasks import tasks


def create_app(
    test_config=None,
):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=path.join(app.instance_path, "taskbox.sqlite"),
    )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)
    try:
        makedirs(app.instance_path)
    except OSError:
        pass
    init_app(app)
    app.register_blueprint(devices)
    app.register_blueprint(runner)
    app.register_blueprint(tasks)
    return app
