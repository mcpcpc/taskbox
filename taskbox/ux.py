#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template

from taskbox.db import query_db

home = Blueprint("home", __name__)


@home.get("/")
def index():
    rows = query_db("select * from tasks order by device")
    cols = ["task_id", "device", "description"]
    task_list = [dict(zip(cols, x)) for x in rows]
    return render_template("index.html", tasks=task_list)
