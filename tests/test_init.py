import unittest

from taskbox import create_app


class InitTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"DATABASE": ":memory:"})
        self.runner = self.app.test_cli_runner()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_db_init_command(self):
        response = self.runner.invoke(args=["init-db"])
        self.assertIn("Initialized", response.output)


if __name__ == "__main__":
    unittest.main()