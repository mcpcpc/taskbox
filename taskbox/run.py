#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import run as subprocess_run
from subprocess import PIPE

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from taskbox.db import get_db

run = Blueprint("run", __name__)


@run.get("/")
def index():
    tasks_v = get_db().execute("select * from task _v").fetchall()
    return render_template("run.html", tasks_v=tasks_v)


@run.get("/run/<int:id>")
def run_task(id: int):
    task = get_db().execute("select * from task where id = ?", (id,)).fetchone()
    command = task["command"]
    result = subprocess_run(command.split(","), stdout=PIPE)
    flash(result.stdout.decode())
    return redirect(url_for("index"))
