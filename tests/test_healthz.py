import unittest
from unittest.mock import patch, MagicMock
from main import app

class TestHealthz(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_healthz(self):
        response = self.app.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    @patch('HTTPLoadTest.requests.get')
    def test_run_load_test_mocked(self, mock_get):
        # Mock the response of requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        payload = {
            "url": "http://example.com",
            "num_requests": 5,
            "concurrency": 2,
            "request_type": "GET"
        }
        response = self.app.post('/run_load_test', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['total_requests'], 5)
        self.assertEqual(data['concurrency'], 2)
        self.assertIn('total_time', data)
        self.assertIn('average_latency', data)
        self.assertIn('percentiles', data)

if __name__ == '__main__':
    unittest.main()
