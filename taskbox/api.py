#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps

from flask import Blueprint
from flask import current_app
from flask import request
from jwt import encode as jwt_encode
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidSignatureError
from jwt.exceptions import ExpiredSignatureError

from taskbox.db import get_db

api = Blueprint("api", __name__, url_prefix="/api")

def token_required(view):
    """View that checks for authentication headers."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if request.authorization is None:
            return "Authorization is missing.", 401
        elif request.authorization["password"] is None:
            return "Token missing.", 401
        token = request.authorization["password"]
        secret_key = current_app.config["SECRET_KEY"]
        try:
            jwt_decode(token, secret_key, algorithms=["HS256"])
        except ExpiredSignatureError:
            return "Token is expired.", 401
        except InvalidSignatureError:
            return "Token has invalid signature.", 401
        return view(**kwargs)
    return wrapped_view


@api.route("/task/<int:id>", methods=("GET",))
@token_required
def read_task(id: int):
    task = get_db().execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    return dict(task)
