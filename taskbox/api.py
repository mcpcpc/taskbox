#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps

from flask import Blueprint
from flask import current_app
from flask import request
from jwt import decode as jwt_decode

from taskbox.db import get_db

api = Blueprint("api", __name__, url_prefix="/api")


def token_required(view):
    """View that checks for authentication headers."""

    @wraps(view)
    def wrapped_view(**kwargs):
        secret_key = current_app.config["SECRET_KEY"]
        try:
            token = request.authorization["password"]
            jwt_decode(token, secret_key, algorithms=["HS256"])
        except Error as error:
            return error, 401
        return view(**kwargs)

    return wrapped_view


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
