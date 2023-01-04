#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from json import loads
from typing import Protocol

from flask import Blueprint
from flask import current_app
from flask import render_template

from taskbox.db import get_db

run = Blueprint("run", __name__)


class Action(Protocol):
    """Task action interface."""

    configuration: dict

    @classmethod
    def jsonify(self) -> dict:
        ...


@run.get("/run/<name>/<int:task_id>")
def action(name: str, task_id: int):
    """Run a specified action by task identifier.
    
    :param name: action name
    :param task_id: task identifier
    :type task_id: int
    
    """
    task = get_db().execute("select * from tasks where task_id = ?", (task_id,)).fetchone()
    if "ACTIONS" not in current_app.config:
        return "No ACTIONS provided in config.py", 400
    if name not in current_app.config["ACTIONS"]:
        return "Not a valid action", 400 
    obj = current_app.config["ACTIONS"][name]
    if not isinstance(obj({}), Action):
        return "Does not conform to Action interface", 400
    obj_loaded = obj(loads(task["actions"]))
    return obj_loaded.jsonify()


@run.app_template_filter()
def fromjson(json_string):
    return loads(json_string)


@run.get("/")
def index():
    tasks = get_db().execute("SELECT * FROM tasks").fetchall()
    return render_template("index.html", tasks=tasks)