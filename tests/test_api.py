import unittest

from taskbox import create_app

DB_TEST_MEM = {"DATABASE": "file::memory:?cache=shared"}

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
        response = self.runner.invoke(args=["init-db"])
        self.assertIn("Initialized", response.output)

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
        pass

    def test_update_task(self):
        pass

    def test_update_task_error(self):
        pass

    def test_delete_task(self):
        pass


if __name__ == "__main__":
    unittest.main()