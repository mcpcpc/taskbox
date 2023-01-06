#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from taskbox.db import get_db

devices = Blueprint("devices", __name__)


@devices.post("/devices")
def create_device():
    db = get_db()
    db.execute(
        "INSERT INTO devices (name, description) VALUES (:name, :description)",
        request.form,
    )
    db.commit()
    return "Device created successfully", 201


@devices.get("/devices/<int:id>")
def read_device(id: int):
    device = (
        get_db().execute("select * from devices where id = ?", (id,)).fetchone()
    )
    if device is None:
        return f"Device {id} does not exist", 404
    return dict(device)


@devices.put("/devices/<int:id>")
def update_device(id: int):
    form = request.form.copy()
    form.add("id", id)
    db = get_db()
    db.execute(
        "UPDATE devices SET name = :name, description = :description WHERE id = :id",
        form,
    )
    db.commit()
    return "Device updated successfully", 201


@devices.delete("/devices/<int:id>")
def delete_device(id: int):
    db = get_db()
    db.execute("DELETE FROM devices WHERE id = ?", (id,))
    db.commit()
    return "Device deleted successfully"
