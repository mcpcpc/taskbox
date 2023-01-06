#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import run
from subprocess import PIPE

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from flask import url_for

from taskbox.db import get_db

runner = Blueprint("runner", __name__)


@runner.get("/")
def index():
    tasks_v = get_db().execute("select * from tasks_v").fetchall()
    return render_template("index.html", tasks_v=tasks_v)


@runner.get("/run/<int:id>")
def run_task(id: int):
    task = get_db().execute("select * from tasks where id = ?", (id,)).fetchone()
    cmd = task["cmd"]
    result = run(cmd.split(","), stdout=PIPE)
    flash(result.stdout.decode())
    return redirect(url_for("runner.index"))
