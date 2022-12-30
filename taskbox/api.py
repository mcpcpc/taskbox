#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from flask import Blueprint
from flask import request

from taskbox.db import modify_db
from taskbox.db import query_db

tasks = Blueprint("tasks", __name__, url_prefix="/api")


def get_slaves(base: str) -> str:
    """Read the list of connected slave EPROMs to master."""
    path = next(Path(base).glob("w1_bus_master*/w1_master_slaves"))
    with open(path, "r") as file:
        content = file.read()
    return content.strip()


def get_nvmem(base: str, slave: str) -> str:
    """Read byte content of attached 1-wire EPROM."""
    path = Path(base) / slave / slave / "nvmem"
    content = b""
    with open(path, "rb") as file:
        file.seek(32)
        while chunk := file.read(32):
            content += chunk[1:-3]
    return content.rstrip(b"\xff")[:-3]


def verify(reference: str, test: str) -> str:
    """Verify content of reference and test string."""
    if reference == test:
        return "Match"
    else:
        return "Does not match"


@tasks.post("/tasks")
def create_task():
    """Post task to tasks list.

    Each device that is intented to be tested shall have a unique task identifier
    characterized by the form parameters below. Upon successful insertion into the task
    database, a unique numeric *task_id* will be generated.

    :form device: typically the assembly part number
    :form description: description of the device
    :form control: validation content

    """
    form = request.form.copy()
    if "file" in request.files:
        file = request.files["file"].read()
        form.add("control", file.decode())
    raw = "INSERT INTO tasks (device, description, control) VALUES (:device, :description, :control)"
    modify_db(raw, form)
    return "Task created successfully", 201


@tasks.get("/tasks/<int:task_id>")
def read_task(task_id: int):
    """Read task by identifier.

    Returns the parameters associated with a specific task identifier. Only one task
    can be returned for a given request.

    :param task_id: task identifier
    :type task_id: int

    """
    return query_db("select * from tasks where task_id = ?", (task_id,))


@tasks.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    """Delete task by identifier.

    When a task is deleted, it will be removed from the list of available tasks.
    Consequently, any action calls associated with the deleted *task_id* will no
    longer be available.

    :param task_id: task identifier
    :type task_id: int

    """
    modify_db("delete from tasks where task_id = ?", (task_id,))
    return f"Task id={task_id} deleted successfully"


@tasks.get("/tasks/<int:task_id>/action")
def task_action(task_id: int):
    """Get task action.

    Returns the results of a specified action, configured per the task identifiers
    parameters.

    :param task_id: task identifier
    :type task_id: int

    """
    control = query_db("select control from tasks where task_id = ?", (task_id,))
    base = "/sys/bus/w1/devices"
    slave = get_slaves(base)
    if "not found" in slave:
        return "No device connected"
    nvmem = get_nvmem(base, slave)
    validation = verify(control[0][0], nvmem.decode(errors="replace"))
    return [slave, validation]
