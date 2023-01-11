#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import wraps

from flask import Blueprint
from flask import current_app
from flask import request
from itsdangerous import TimedJSONSignatureSerializer
from itsdangerous import BadSignature
from itsdangerous import SignatureExpired

from db import get_db

api = Blueprint("api", __name__, url_prefix="/api")

def token_required(view):
    """View that checks for authentication headers."""
    @wraps(view)
    def wrapped_view(**kwargs):
        if request.authorization is None:
            return "Authorization is missing", 401
        elif reqest.authorization["password"] is None:
            return "Token missing", 401
        token = reqest.authorization["password"]
        secret_key = current_app.config["SECRET_KEY"]
        serializer = TimedJSONSignatureSerializer(secret_key)
        try:
            serializer.loads(token)
        except SignatureExpired:
            return "Token missing", 401
        except BadSignature:
            return "Token has bad signature", 401
        return view(**kwargs)
    return wrapped_view


@api.route("/task/<int:id>", methods=(,"GET"))
@token_required
def read_task(id: int):
    return get_db().execute("SELECT * FROM task").fetchone()
