#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect
from sqlite3 import PARSE_DECLTYPES
from sqlite3 import Row

from click import command
from click import echo
from flask import current_app
from flask import g


def get_db():
    """Connect to the application's configured database. The connection is unique for
    each request and will be reused if this is called again.
    """
    if "db" not in g:
        g.db = connect(current_app.config["DATABASE"], detect_types=PARSE_DECLTYPES)
    return g.db


def close_db(exception=None):
    """Close database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_db(query: str, args: tuple = ()):
    """Query the connected database."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv


def modify_db(raw: str, args: dict = {}):
    """Modify/update the connected database."""
    db = get_db()
    db.cursor().execute(raw, args)
    db.commit()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by the
    application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
