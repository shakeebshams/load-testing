import unittest
from unittest.mock import patch, MagicMock
import requests
from HTTPLoadTest import HTTPLoadTest

class TestHTTPLoadTest(unittest.TestCase):
    @patch('requests.get')
    def test_successful_run(self, mock_get):
        # Mock a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        test = HTTPLoadTest(url="http://example.com", num_requests=5, concurrency=2, request_type="GET")
        test.run_test()

        self.assertEqual(test.errors, 0)
        self.assertEqual(len(test.latencies), 5)
        self.assertGreater(test.average_latency, 0.0)
        self.assertEqual(len(test.percentiles), 4)
        for p in ["percentile_50th", "percentile_75th", "percentile_95th", "percentile_99th"]:
            self.assertIn(p, test.percentiles)
            self.assertGreater(test.percentiles[p], 0.0)

    @patch('requests.get')
    def test_all_failed_run(self, mock_get):
        # Mock a failed response (raise_for_status raises an exception)
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")
        mock_get.return_value = mock_response

        test = HTTPLoadTest(url="http://example.com", num_requests=5, concurrency=2, request_type="GET")
        test.run_test()

        self.assertEqual(test.errors, 5)
        self.assertEqual(len(test.latencies), 0)
        self.assertEqual(test.average_latency, 0.0)
        self.assertEqual(len(test.percentiles), 4)
        for p in ["percentile_50th", "percentile_75th", "percentile_95th", "percentile_99th"]:
            self.assertIn(p, test.percentiles)
            self.assertEqual(test.percentiles[p], 0.0)

    @patch('requests.post')
    def test_post_successful_run(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        test = HTTPLoadTest(url="http://example.com", num_requests=3, concurrency=1, request_type="POST", data={"key": "value"})
        test.run_test()

        self.assertEqual(test.errors, 0)
        self.assertEqual(len(test.latencies), 3)
        self.assertGreater(test.average_latency, 0.0)
        self.assertEqual(len(test.percentiles), 4)

    @patch('requests.get')
    def test_mixed_run(self, mock_get):
        # Mock mixed success and failure
        mock_success = MagicMock()
        mock_failure = MagicMock()
        mock_failure.raise_for_status.side_effect = requests.exceptions.HTTPError("HTTP Error")

        # 3 successes, then 2 failures
        mock_get.side_effect = [mock_success, mock_success, mock_success, mock_failure, mock_failure]

        test = HTTPLoadTest(url="http://example.com", num_requests=5, concurrency=1, request_type="GET")
        test.run_test()

        self.assertEqual(test.errors, 2)
        self.assertEqual(len(test.latencies), 3)
        self.assertGreater(test.average_latency, 0.0)
        self.assertEqual(len(test.percentiles), 4)
        for p in ["percentile_50th", "percentile_75th", "percentile_95th", "percentile_99th"]:
            self.assertIn(p, test.percentiles)
            self.assertGreater(test.percentiles[p], 0.0)

    def test_unsupported_request_type(self):
        test = HTTPLoadTest(url="http://example.com", num_requests=1, concurrency=1, request_type="PUT")
        test.run_test()
        self.assertEqual(test.errors, 1)
        self.assertEqual(len(test.latencies), 0)
        self.assertEqual(test.average_latency, 0.0)
        self.assertEqual(len(test.percentiles), 4)
        for p in ["percentile_50th", "percentile_75th", "percentile_95th", "percentile_99th"]:
            self.assertIn(p, test.percentiles)
            self.assertEqual(test.percentiles[p], 0.0)

if __name__ == '__main__':
    unittest.main()
