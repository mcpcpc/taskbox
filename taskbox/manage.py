#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from taskbox.db import get_db
from taskbox.auth import login_required

manage = Blueprint("manage", __name__, url_prefix="/manage")


@manage.get("/")
@login_required
def index():
    devices = get_db().execute("select * from devices").fetchall()
    tasks = get_db().execute("select * from tasks").fetchall()
    users = get_db().execute("select * from users").fetchall()
    return render_template(
        "manage/manage.html", devices=devices, tasks=tasks, users=users
    )


@manage.route("/tasks/create", methods=("GET", "POST"))
@login_required
def create_task():
    if request.method == "POST":
        error = None
        device_id = request.form["device_id"]
        name = request.form["name"]
        command = request.form["command"]
        if not name:
            error = "Name is required."
        elif not command:
            error = "Command is required."
        elif not device_id:
            error = "Device ID is required."
        if error is None:
            try:
                db = get_db()
                db.execute('PRAGMA foreign_keys = ON')
                db.execute(
                    "INSERT INTO tasks (name, command, device_id) VALUES (?, ?, ?)",
                    (name, command, device_id),
                )
                db.commit()
            except db.IntegrityError:
                error = "Device ID does not exist."
            else:
                return redirect(url_for("manage.index"))
        flash(error)
    return render_template("manage/create_task.html")


@manage.route("/tasks/<int:id>/update", methods=("GET", "POST"))
@login_required
def update_task(id: int):
    db = get_db()
    device = db.execute("SELECT * FROM tasks WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        error = None
        device_id = request.form["device_id"]
        name = request.form["name"]
        command = request.form["command"]
        if not name:
            error = "Name is required."
        elif not command:
            error = "Command is required."
        elif not device_id:
            error = "Device ID is required."
        if error is None:
            db.execute('PRAGMA foreign_keys = ON')
            try:
                db.execute(
                    "UPDATE tasks SET device_id = ?, name = ?, command = ? WHERE id = ?",
                    (device_id, name, command, id),
                )
                db.commit()
            except db.IntegrityError:
                error = "Device ID does not exist."
            else:
                return redirect(url_for("manage.index"))
        flash(error)
    return render_template("manage/update_task.html", device=device)


@manage.route("/tasks/<int:id>/delete", methods=("GET",))
@login_required
def delete_task(id: int):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("manage.index"))


@manage.route("/devices/create", methods=("GET", "POST"))
@login_required
def create_device():
    if request.method == "POST":
        db = get_db()
        try:
            db.execute('PRAGMA foreign_keys = ON')
            db.execute(
                "INSERT INTO devices (name, description) VALUES (:name, :description)",
                request.form,
            )
            db.commit()
        except db.IntegrityError:
            flash("Device already exists", "error")
            return redirect(url_for("manage.create_device"))
        return redirect(url_for("manage.index"))
    return render_template("manage/create_device.html")


@manage.route("/devices/<int:id>/update", methods=("GET", "POST"))
@login_required
def update_device(id: int):
    db = get_db()
    device = db.execute("SELECT * FROM devices WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        db.execute(
            "UPDATE devices SET name = ?, description = ? WHERE id = ?",
            (name, description, id),
        )
        db.commit()
        return redirect(url_for("manage.index"))
    return render_template("manage/update_device.html", device=device)


@manage.route("/devices/<int:id>/delete", methods=("GET",))
@login_required
def delete_device(id: int):
    db = get_db()
    db.execute('PRAGMA foreign_keys = ON')
    db.execute("DELETE FROM devices WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("manage.index"))
