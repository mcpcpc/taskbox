import unittest

from taskbox import create_app

DB_TEST_MEM = {"DATABASE": ":memory:"}

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(DB_TEST_MEM)
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.client = self.app.test_client()
        self.runner = self.app.test_cli_runner()

    def tearDown(self):
        self.ctx.pop()

    def test_db_init_command(self):
        result = self.runner.invoke(
            args=["init-db"]
        )
        self.assertIn("Initialized", result.output)

    def test_create_task(self):
        result = self.client.post(
            "/api/tasks",
            data={
                "device": "device1",
                "description: "description1",
                "control": "control1"
            }
        )
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main()
