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
        self.app = create_app({"TESTING": True, "DATABASE": self.db})
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

    def test_delete_device(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.get("/manage/devices/1/delete", follow_redirects=True)
        self.assertIn(b"Device deleted successfully", response.data)

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

    def test_delete_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post(
            "/auth/login",
            data={"username": "test", "password": "test"},
        )
        response = self.client.get("/manage/tasks/1/delete", follow_redirects=True)
        self.assertIn(b"Task deleted successfully", response.data)


if __name__ == "__main__":
    main()
