#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import render_template

from taskbox.db import get_db

home = Blueprint("home", __name__)


@home.get("/")
def index():
    tasks = get_db().execute("select * from tasks order by device").fetchall()
    return render_template("index.html", tasks=tasks)
