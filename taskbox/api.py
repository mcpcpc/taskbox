#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from flask import Blueprint
from flask import request

from taskbox.database import modify_db
from taskbox.database import query_db

tasks = Blueprint("tasks", __name__, url_prefix='/api')


def get_slaves(base: str) -> str:
    """"""
    path = next(Path(base).glob("w1_bus_master*/w1_master_slaves"))
    with open(path, "r") as file:
        content = file.read()
    return content.strip()


def get_nvmem(base: str, slave: str) -> str:
    """Read byte content of attached 1-wire EPROM."""
    path = Path(base) / slave / slave / "nvmem"
    with open(path, "rb") as file:
        file.seek(32)
        content = file.read()
    return content.rstrip(b"\xff")


@tasks.post("/tasks")
def create_task():
    """Post task to tasks list.
    
    Each device that is intented to be tested shall have
    a unique task identifier characterized by the form
    parameters below. Upon successful insertion into the
    task database, a unique numeric *task_id* will be 
    generated.
    
    :form device: typically the assembly part number
    :form description: description of the device
    :form control: validation content
    
    """
    form = request.form.copy()
    if "file" in request.files:
        file = request.files["file"].read()
        form["control"] = file.decode()
    raw = (
        "INSERT INTO tasks (device, description, control) "
        "VALUES (:device, :description, :control)"
    )
    modify_db(raw, form)
    return "Task created successfully", 201


@tasks.get("/tasks/<int:task_id>")
def read_task(task_id: int):
    """Read task by identifier.
    
    Returns the parameters associated with a specific
    task identifier. Only one task can be returned for
    a given request.
    
    :param task_id: task identifier
    :type task_id: int
    
    """
    raw = "select * from tasks where task_id = ?"
    return query_db(raw, (task_id,))


@tasks.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    """Delete task by identifier.
    
    When a task is deleted, it will be removed from the
    list of available tasks. Consequently, any action
    calls associated with the deleted *task_id* will no
    longer be available.
    
    :param task_id: task identifier
    :type task_id: int
    
    """
    raw = "delete from tasks where task_id = ?"
    modify_db(raw, (task_id,))
    return f"Task id={task_id} deleted successfully"