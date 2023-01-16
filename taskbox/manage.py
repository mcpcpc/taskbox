#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for
from jwt import encode as jwt_encode

from taskbox.db import get_db
from taskbox.auth import login_required

manage = Blueprint("manage", __name__, url_prefix="/manage")


@manage.get("/")
@login_required
def index():
    users_v = get_db().execute("select * from user_v").fetchall()
    devices = get_db().execute("select * from device").fetchall()
    tasks = get_db().execute("select * from task").fetchall()
    tests = get_db().execute("select * from test").fetchall()
    return render_template(
        "manage/manage.html", devices=devices, tests=tests, tasks=tasks, users_v=users_v
    )


@manage.route("/test/create", methods=("GET", "POST"))
@login_required
def create_test():
    db = get_db()
    devices = db.execute("SELECT * FROM device").fetchall()
    if request.method == "POST":
        error = None
        device_id = request.form["device_id"]
        name = request.form["name"]
        description = request.form["description"]
        if not name:
            error = "Name is required."
        elif not description:
            error = "Description is required."
        elif not device_id:
            error = "Device ID is required."
        if error is None:
            try:
                db.execute("PRAGMA foreign_keys = ON")
                db.execute(
                    "INSERT INTO test (name, description, device_id) VALUES (?, ?, ?)",
                    (name, description, device_id),
                )
                db.commit()
            except db.IntegrityError:
                error = "Device ID does not exist."
            else:
                return redirect(url_for("manage.index"))
        flash(error, "error")
    return render_template("manage/create_test.html", devices=devices)


@manage.route("/test/<int:id>/update", methods=("GET", "POST"))
@login_required
def update_test(id: int):
    db = get_db()
    test = db.execute("SELECT * FROM test WHERE id = ?", (id,)).fetchone()
    devices = db.execute("SELECT * FROM device").fetchall()
    if request.method == "POST":
        error = None
        device_id = request.form["device_id"]
        name = request.form["name"]
        description = request.form["description"]
        if not name:
            error = "Name is required."
        elif not description:
            error = "Description is required."
        elif not device_id:
            error = "Device ID is required."
        if error is None:
            db.execute("PRAGMA foreign_keys = ON")
            try:
                db.execute(
                    "UPDATE test SET device_id = ?, name = ?, description = ? WHERE id = ?",
                    (device_id, name, description, id),
                )
                db.commit()
            except db.IntegrityError:
                error = "Device ID does not exist."
            else:
                return redirect(url_for("manage.index"))
        flash(error, "error")
    return render_template("manage/update_test.html", test=test, devices=devices)


@manage.route("/test/<int:id>/delete", methods=("GET",))
@login_required
def delete_test(id: int):
    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM test WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("manage.index"))


@manage.route("/tasks/create", methods=("GET", "POST"))
@login_required
def create_task():
    db = get_db()
    tests = db.execute("SELECT * FROM test").fetchall()
    if request.method == "POST":
        error = None
        test_id = request.form["test_id"]
        name = request.form["name"]
        command = request.form["command"]
        if not name:
            error = "Name is required."
        elif not command:
            error = "Command is required."
        elif not test_id:
            error = "Test ID is required."
        if error is None:
            try:
                db.execute("PRAGMA foreign_keys = ON")
                db.execute(
                    "INSERT INTO task (name, command, test_id) VALUES (?, ?, ?)",
                    (name, command, test_id),
                )
                db.commit()
            except db.IntegrityError:
                error = "Test ID does not exist."
            else:
                return redirect(url_for("manage.index"))
        flash(error, "error")
    return render_template("manage/create_task.html", tests=tests)


@manage.route("/tasks/<int:id>/update", methods=("GET", "POST"))
@login_required
def update_task(id: int):
    db = get_db()
    task = db.execute("SELECT * FROM task WHERE id = ?", (id,)).fetchone()
    tests = db.execute("SELECT * FROM test").fetchall()
    if request.method == "POST":
        error = None
        test_id = request.form["test_id"]
        name = request.form["name"]
        command = request.form["command"]
        if not name:
            error = "Name is required."
        elif not command:
            error = "Command is required."
        elif not test_id:
            error = "Test ID is required."
        if error is None:
            db.execute("PRAGMA foreign_keys = ON")
            try:
                db.execute(
                    "UPDATE task SET test_id = ?, name = ?, command = ? WHERE id = ?",
                    (test_id, name, command, id),
                )
                db.commit()
            except db.IntegrityError:
                error = "Test ID does not exist."
            else:
                return redirect(url_for("manage.index"))
        flash(error, "error")
    return render_template("manage/update_task.html", task=task, tests=tests)


@manage.route("/tasks/<int:id>/delete", methods=("GET",))
@login_required
def delete_task(id: int):
    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM task WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("manage.index"))


@manage.route("/device/create", methods=("GET", "POST"))
@login_required
def create_device():
    if request.method == "POST":
        db = get_db()
        try:
            db.execute("PRAGMA foreign_keys = ON")
            db.execute(
                "INSERT INTO device (name, description) VALUES (:name, :description)",
                request.form,
            )
            db.commit()
        except db.IntegrityError:
            flash("Device already exists", "error")
            return redirect(url_for("manage.create_device"))
        return redirect(url_for("manage.index"))
    return render_template("manage/create_device.html")


@manage.route("/device/<int:id>/update", methods=("GET", "POST"))
@login_required
def update_device(id: int):
    db = get_db()
    device = db.execute("SELECT * FROM device WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        error = None
        name = request.form["name"]
        description = request.form["description"]
        if not name:
            error = "Name is required."
        elif not description:
            error = "Description is required."
        if error is None:
            db.execute(
                "UPDATE device SET name = ?, description = ? WHERE id = ?",
                (name, description, id),
            )
            db.commit()
            return redirect(url_for("manage.index"))
        flash(error)
        return redirect(url_for("manage.update_device", id=id))
    return render_template("manage/update_device.html", device=device)


@manage.route("/device/<int:id>/delete", methods=("GET",))
@login_required
def delete_device(id: int):
    db = get_db()
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("DELETE FROM device WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("manage.index"))
