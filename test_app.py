
import unittest

from app import app


class WebsiteMonitorTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_website(self):
        response = self.client.post(
            "/api/add",
            json={"url": "https://example.com"}
        )

        self.assertEqual(response.status_code, 201)

    def test_invalid_website(self):
        response = self.client.post(
            "/api/add",
            json={"url": "invalid-url"}
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
