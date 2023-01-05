#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from taskbox import create_app


class Dummy:
    def __init__(self, configuration):
        self.configuration = configuration

    @classmethod
    def jsonify(self):
        return "OK"


class RunTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._resources = Path(__file__).parent
        path = cls._resources / "preload.sql"
        with open(path, mode="r", encoding="utf-8") as f:
            cls._preload = f.read()

    def setUp(self):
        self.db = "file::memory:?cache=shared"
        self.app = create_app({"DATABASE": self.db, "ACTIONS": {"dummy": Dummy}})
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_cli_runner().invoke(args=["init-db"])

    def tearDown(self):
        self.ctx.pop()

    def test_run_action(self):
        db = connect(self.db)
        db.executescript(self._preload)
        response = self.client.get("/run/dummy/1")
        self.assertEqual(response.status_code, 200)
