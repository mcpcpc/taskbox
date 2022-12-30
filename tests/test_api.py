import unittest

from taskbox import create_app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = create_app.app_context()
        self.ctx.push()
        self.client = app.test_client()
    
    def tearDown(self):
        self.ctx.pop()

if __name__ == "__main__":
    unittest.main()
