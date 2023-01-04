#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from taskbox.db import get_db

tasks = Blueprint("tasks", __name__)


@tasks.post("/tasks")
def create_task():
    """Post task to tasks list.

    Each device that is intented to be tested shall have a unique task identifier
    characterized by the form parameters below. Upon successful insertion into the task
    database, a unique numeric *task_id* will be generated.

    :form device: typically the assembly part number
    :form description: description of the device
    :form actions: JSON string formatted action configuration

    """
    db = get_db()
    db.execute("INSERT INTO tasks (device, description, actions) VALUES (:device, :description, :actions)", request.form)
    db.commit()
    return "Task created successfully", 201


@tasks.get("/tasks/<int:task_id>")
def read_task(task_id: int):
    """Read task by identifier.

    Returns the parameters associated with a specific task identifier. Only one task
    can be returned for a given request.

    :param task_id: task identifier
    :type task_id: int

    """
    task = get_db().execute("select * from tasks where task_id = ?", (task_id,)).fetchone()
    if task is None:
        return f"Task {task_id} does not exist", 404
    return dict(task)


@tasks.put("/tasks/<int:task_id>")
def update_task(task_id: int):
    """Update task by identifier.

    Same as task creation but able to update task fields based on the identifier.

    :form device: typically the assembly part number
    :form description: description of the device
    :form actions: JSON string formatted action configuration

    """
    form = request.form.copy()
    form.add("task_id", task_id)
    db = get_db()
    db.execute("UPDATE tasks SET device = :device, description = :description, actions = :actions WHERE task_id = :task_id", form)
    db.commit()
    return "Task updated successfully", 201


@tasks.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    """Delete task by identifier.

    When a task is deleted, it will be removed from the list of available tasks.
    Consequently, any action calls associated with the deleted *task_id* will no
    longer be available.

    :param task_id: task identifier
    :type task_id: int

    """
    db = get_db()
    db.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
    db.commit()
    return "Task deleted successfully"
