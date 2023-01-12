#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from taskbox import create_app


class ManageTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._resources = Path(__file__).parent
        path = cls._resources / "preload.sql"
        with open(path, mode="r", encoding="utf-8") as f:
            cls._preload = f.read()

    def setUp(self):
        self.db = "file::memory:?cache=shared"
        self.app = create_app(
            {"TESTING": True, "DATABASE": self.db, "SECRET_KEY": "dev"}
        )
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_cli_runner().invoke(args=["init-db"])

    def tearDown(self):
        self.ctx.pop()

    def test_create_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.post(
            "/manage/devices/create",
            data={"name": "name2", "description": "description2"},
        )
        self.assertEqual(response.headers["location"], "/manage/")

    def test_update_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.post(
            "/manage/devices/1/update",
            data={"name": "name1_", "description": "description1_"},
        )
        self.assertEqual(response.headers["location"], "/manage/")

    def test_delete_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.get("/manage/devices/1/delete")
        self.assertEqual(response.headers["location"], "/manage/")

    def test_create_device_flash(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        parameters = [("name1", "description1", b"Device already exists")]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                name, description, message = parameter
                response = self.client.post(
                    "/manage/devices/create",
                    data={"name": name, "description": message},
                    follow_redirects=True,
                )
                self.assertIn(message, response.data)

    def test_create_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.post(
            "/manage/tasks/create",
            data={"name": "name2", "device_id": 1, "command": "command2"},
        )
        self.assertEqual(response.headers["location"], "/manage/")

    def test_create_task_flash(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        parameters = [
            ("", "name1", "command1", b"Device ID is required"),
            ("1", "", "command1", b"Name is required"),
            ("1", "name1", "", b"Command is required"),
            ("2", "name1", "command1", b"Device ID does not exist"),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                device_id, name, command, message = parameter
                response = self.client.post(
                    "/manage/tasks/create",
                    data={"device_id": device_id, "name": name, "command": command},
                    follow_redirects=True,
                )
                self.assertIn(message, response.data)

    def test_update_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.post(
            "/manage/tasks/1/update",
            data={"name": "name2_", "device_id": 1, "command": "command2_"},
        )
        self.assertEqual(response.headers["location"], "/manage/")

    def test_update_task_flash(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        parameters = [
            ("", "name1", "command1", b"Device ID is required"),
            ("1", "", "command1", b"Name is required"),
            ("1", "name1", "", b"Command is required"),
            ("2", "name1", "command1", b"Device ID does not exist"),
        ]
        for parameter in parameters:
            with self.subTest(parameter=parameter):
                device_id, name, command, message = parameter
                response = self.client.post(
                    "/manage/tasks/1/update",
                    data={"device_id": device_id, "name": name, "command": command},
                    follow_redirects=True,
                )
                self.assertIn(message, response.data)

    def test_delete_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.get("/manage/tasks/1/delete")
        self.assertEqual(response.headers["location"], "/manage/")


if __name__ == "__main__":
    main()
