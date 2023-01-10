from functools import wraps

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from taskbox.db import get_db

auth = Blueprint("auth", __name__)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@auth.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@auth.route("/auth/register", methods=("GET", "POST"))
@login_required
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    db = get_db()
    roles = db.execute("SELECT * FROM role").fetchall()
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role_id = request.form["role_id"]
        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not role_id:
             error = "Role ID is required."
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (role_id, username, password) VALUES (?, ?, ?)",
                    (role_id, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error, "error")
    return render_template("auth/register.html", roles=roles)


@auth.route("/auth/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id: int):
    """Update an existing users password."""
    db = get_db()
    user = get_db().execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        password = request.form["password"]
        error = None
        if not password:
            error = "Password is required."
        if error is None:
            db.execute(
                "UPDATE user SET password = ? WHERE id = ?",
                (generate_password_hash(password), id),
            )
            db.commit()
            if session.get("user_id") == id:
                session.clear()
                return redirect(url_for("auth.login"))
            return redirect(url_for("manage.index"))
        flash(error, "error")
    return render_template("auth/update.html", user=user)


@auth.route("/auth/<int:id>/delete", methods=("GET",))
@login_required
def delete(id: int):
    db = get_db()
    db.execute("DELETE FROM user WHERE id = ?", (id,))
    db.commit()
    if session.get("user_id") == id:
        session.clear()
    return redirect(url_for("manage.index"))


@auth.route("/auth/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            error = "Incorrect username or password."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect username or password."
        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        flash(error, "error")
    return render_template("auth/login.html")


@auth.route("/auth/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
