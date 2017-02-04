import unittest

from server import app
from model import db, connect_to_db


class RatingsTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("Ratings", result.data)



if __name__ == "__main__":
    unittest.main()
