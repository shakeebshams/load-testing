import unittest
from main import app

class TestHealthz(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_healthz_status_code(self):
        response = self.app.get('/healthz')
        self.assertEqual(response.status_code, 200)

    def test_healthz_json_response(self):
        response = self.app.get('/healthz')
        data = response.get_json()
        self.assertEqual(data, {"status": "ok"})

    def test_healthz_method_not_allowed(self):
        response = self.app.post('/healthz')
        self.assertEqual(response.status_code, 405)
