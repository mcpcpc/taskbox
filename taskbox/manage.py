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
    return render_template("manage/manage.html", devices=devices, tasks=tasks)


@manage.route("/tasks/create", methods=("GET", "POST"))
@login_required
def create_task():
    if request.method == "POST":
        db = get_db()
        try:
            db.execute("INSERT INTO tasks (name, command, device_id) VALUES (:name, :command, :device_id)", request.form)
            db.commit()
        except db.IntegrityError:
            flash("Task already exists")
            return redirect(url_for("manage.create_task"))
        flash("Task created successfully")
        return redirect(url_for("manage.index"))
    return render_template("manage/create_task.html")


@manage.route("/tasks/<int:id>/delete", methods=("GET",))
@login_required
def delete_task(id: int):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (id,))
    db.commit()
    flash("Task deleted successfully")
    return redirect(url_for("manage.index"))


@manage.route("/devices/create", methods=("GET", "POST"))
@login_required
def create_device():
    if request.method == "POST":
        db = get_db()
        try:
            db.execute("INSERT INTO devices (name, description) VALUES (:name, :description)", request.form)
            db.commit()
        except db.IntegrityError:
            flash("Task already exists")
            return redirect(url_for("manage.create_device"))
        flash("Device created successfully")
        return redirect(url_for("manage.index"))
    return render_template("manage/create_device.html")


@manage.route("/devices/<int:id>/delete", methods=("GET",))
@login_required
def delete_device(id: int):
    db = get_db()
    db.execute("DELETE FROM devices WHERE id = ?", (id,))
    db.commit()
    flash("Device deleted successfully")
    return redirect(url_for("manage.index"))

