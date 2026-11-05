import unittest
from unittest.mock import patch, MagicMock
import json
from main import app

class TestHealthzAndLoadTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_healthz(self):
        response = self.app.get('/healthz')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data, {"status": "ok"})

    @patch('HTTPLoadTest.requests.get')
    def test_run_load_test_mocked(self, mock_get):
        # Mock the response of requests.get
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        payload = {
            "url": "http://mocked-url.com",
            "num_requests": 5,
            "concurrency": 2,
            "request_type": "GET"
        }
        response = self.app.post('/run_load_test', 
                                 data=json.dumps(payload),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["total_requests"], 5)
        self.assertEqual(data["concurrency"], 2)
        self.assertEqual(data["errors"], 0)
        self.assertIn("total_time", data)
        self.assertIn("average_latency", data)
        self.assertIn("percentiles", data)
        
        # Verify that requests.get was called 5 times
        self.assertEqual(mock_get.call_count, 5)

if __name__ == '__main__':
    unittest.main()
