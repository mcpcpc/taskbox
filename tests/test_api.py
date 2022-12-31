from pathlib import Path
from sqlite3 import connect
from unittest import main
from unittest import TestCase

from taskbox import create_app


class ApiTestCase(TestCase):
    def setUp(self):
        self.db = "file::memory:?cache=shared"
        self.app = create_app({"DATABASE": self.db})
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.app.test_cli_runner().invoke(args=["init-db"])

    def tearDown(self):
        self.ctx.pop()
 
    def test_create_task(self):
        response = self.client.post(
            "/api/tasks",
            data={
                "device": "device1",
                "description": "description1",
                "control": "control1"
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_read_task(self):
        path = Path(__file__).parent / "payload.sql"
        db = connect(self.db)
        with open(path, mode="r", encoding="utf-8") as f:
            db.executescript(f.read())
        response = self.client.get("/api/tasks/1")
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        pass

    def test_update_task_error(self):
        pass

    def test_delete_task(self):
        path = Path(__file__).parent / "payload.sql"
        db = connect(self.db)
        with open(path, mode="r", encoding="utf-8") as f:
            db.executescript(f.read())
        response = self.client.delete("/api/tasks/1")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    main()