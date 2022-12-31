from unittest import main
from unittest import TestCase

from taskbox import create_app


class InitTestCase(TestCase):
    def setUp(self):
        self.db = ":memory:"
        self.app = create_app({"DATABASE": self.db})
        self.runner = self.app.test_cli_runner()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_db_init_command(self):
        response = self.runner.invoke(args=["init-db"])
        self.assertIn("Initialized", response.output)


if __name__ == "__main__":
    main()