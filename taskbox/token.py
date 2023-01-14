#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from functools import wraps

from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import flash
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from taskbox.db import get_db
from taskbox.auth import login_required

token = Blueprint("token", __name__, url_prefix="/token")


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


@token.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        error = None
        if not request.form["expires_in"]:
            error = "Expires In is required."
        if int(request.form["expires_in"]) > 31536000:
            error = "Expires In is too big."
        if error is None:
            expires_in = int(request.form["expires_in"])
            exp = datetime.now(tz=timezone.utc) + timedelta(seconds=expires_in)
            token = jwt_encode(
                dict(confirm=session.get("user_id"), exp=exp),
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            return {"access_token": token}
        flash(error)
        return redirect(url_for("token.create", id=id))
    return render_template("token/create.html")
