from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from taskbox import create_app


class UxTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).parent / "preload.sql"
        with open(path, mode="r", encoding="utf-8") as f:
            cls._preload = f.read()

    def setUp(self):
        self.db = "file::memory:?cache=shared"
        self.app = create_app({"DATABASE": self.db})
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_cli_runner().invoke(args=["init-db"])

    def tearDown(self):
        self.ctx.pop()

    def test_index(self):
        db = connect(self.db)
        db.executescript(self._preload)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    main()
