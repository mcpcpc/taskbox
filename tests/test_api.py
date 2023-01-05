#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from taskbox import create_app


class ApiTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._resources = Path(__file__).parent
        path = cls._resources / "preload.sql"
        with open(path, mode="r", encoding="utf-8") as f:
            cls._preload = f.read()

    def setUp(self):
        self.db = "file::memory:?cache=shared"
        self.app = create_app(
            {"TESTING": True, "DATABASE": self.db}
        )
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_cli_runner().invoke(args=["init-db"])

    def tearDown(self):
        self.ctx.pop()

    def test_create_task(self):
        response = self.client.post(
            "/tasks",
            data={
                "device": "device1",
                "description": "description1",
                "actions": "actions1",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_read_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        response = self.client.get("/tasks/1")
        self.assertEqual(response.status_code, 200)

    def test_read_task_doesnt_exist(self):
        db = connect(self.db)
        db.executescript(self._preload)
        response = self.client.get("/tasks/2")
        self.assertEqual(response.status_code, 404)

    def test_update_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        response = self.client.put(
            "/tasks/1",
            data={
                "device": "device1_",
                "description": "description1_",
                "actions": "actions1_",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_delete_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        response = self.client.delete("/tasks/1")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    main()
