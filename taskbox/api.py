#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps

from flask import Blueprint
from flask import current_app
from flask import request

from taskbox.db import get_db
from taskbox.token import token_required

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/task/<int:id>", methods=("GET",))
@token_required
def read_task(id: int):
    task = get_db().execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    return dict(task)


@api.route("/device/<int:id>", methods=("GET",))
@token_required
def read_device(id: int):
    device = get_db().execute("SELECT * FROM device WHERE id = ?", (id,)).fetchone()
    return dict(device)
