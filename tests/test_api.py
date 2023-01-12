#!/usr/bin/env python
# -*- coding: utf-8 -*-

from base64 import b64encode

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
                {"TESTING": True, "DATABASE": self.db, "SECRET_KEY": "dev"}
        )
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_cli_runner().invoke(args=["init-db"])

    def tearDown(self):
        self.ctx.pop()

    def test_read_task_get(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        response = self.client.get("/manage/user/1/token")
        self.assertEqual(response.status_code, 200)

    def test_read_task(self):
        db = connect(self.db)
        db.executescript(self._preload)
        self.client.post("/auth/login", data={"username": "test", "password": "test"})
        data = self.client.post("/manage/user/1/token", data={"expires_in": 600})
        token_encoded = b64encode(f":{data.json['token']}".encode("utf-8")).decode("utf-8")
        response = self.client.get("/api/task/1", headers={"Authorization": f"Basic {token_encoded}"})
        self.assertEqual(response.status_code, 200)

