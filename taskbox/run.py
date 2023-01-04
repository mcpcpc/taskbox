#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Protocol
from json import loads

from flask import Blueprint
from flask import current_app

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
    configuration = get_db().execute("select actions from tasks where task_id = ?", (task_id,)).fetchone()
    if "ACTIONS" not in current_app.config:
        return "No ACTIONS provided in config.py", 400
    if name not in current_app.config["ACTIONS"]:
        return "Not a valid action", 400 
    obj = current_app.config["ACTIONS"][name]
    if not isinstance(obj({}), Action):
        return "Does not conform to Action interface", 400
    obj_loaded = obj(loads(configuration))
    return obj_loaded.jsonify()
