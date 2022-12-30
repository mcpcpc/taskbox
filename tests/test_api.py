import unittest

from taskbox import create_app


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
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


if __name__ == "__main__":
    unittest.main()
