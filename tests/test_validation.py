import unittest
from unittest.mock import patch, MagicMock
from HTTPLoadTest import HTTPLoadTest

class TestHTTPLoadTestValidation(unittest.TestCase):
    def test_valid_inputs(self):
        # Valid positive integers should not raise any error
        try:
            test = HTTPLoadTest(url="http://example.com", num_requests=10, concurrency=2)
        except ValueError as e:
            self.fail(f"HTTPLoadTest raised ValueError unexpectedly: {e}")
        
        self.assertEqual(test.num_requests, 10)
        self.assertEqual(test.concurrency, 2)

    def test_invalid_num_requests_type(self):
        # num_requests must be an integer, not float, string, list, dict, or bool
        invalid_types = [10.5, "10", [10], {"num": 10}, True, False]
        for val in invalid_types:
            with self.subTest(val=val):
                with self.assertRaises(ValueError) as ctx:
                    HTTPLoadTest(url="http://example.com", num_requests=val, concurrency=2)
                self.assertIn("num_requests must be a positive integer", str(ctx.exception))

    def test_invalid_num_requests_value(self):
        # num_requests must be positive (> 0)
        invalid_values = [0, -1, -100]
        for val in invalid_values:
            with self.subTest(val=val):
                with self.assertRaises(ValueError) as ctx:
                    HTTPLoadTest(url="http://example.com", num_requests=val, concurrency=2)
                self.assertIn("num_requests must be a positive integer", str(ctx.exception))

    def test_invalid_concurrency_type(self):
        # concurrency must be an integer, not float, string, list, dict, or bool
        invalid_types = [2.5, "2", [2], {"concurrency": 2}, True, False]
        for val in invalid_types:
            with self.subTest(val=val):
                with self.assertRaises(ValueError) as ctx:
                    HTTPLoadTest(url="http://example.com", num_requests=10, concurrency=val)
                self.assertIn("concurrency must be a positive integer", str(ctx.exception))

    def test_invalid_concurrency_value(self):
        # concurrency must be positive (> 0)
        invalid_values = [0, -1, -100]
        for val in invalid_values:
            with self.subTest(val=val):
                with self.assertRaises(ValueError) as ctx:
                    HTTPLoadTest(url="http://example.com", num_requests=10, concurrency=val)
                self.assertIn("concurrency must be a positive integer", str(ctx.exception))

    @patch('requests.get')
    def test_run_test_with_mocked_network(self, mock_get):
        # Mock the response to avoid real network traffic
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        test = HTTPLoadTest(url="http://example.com", num_requests=5, concurrency=2)
        test.run_test()

        self.assertEqual(mock_get.call_count, 5)
        self.assertEqual(len(test.latencies), 5)
        self.assertEqual(test.errors, 0)
        self.assertIsNotNone(test.average_latency)
        self.assertIsNotNone(test.total_time)
        self.assertIn("percentile_50th", test.percentiles)
