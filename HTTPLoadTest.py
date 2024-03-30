import time
import requests
import numpy as np


class HTTPLoadTest:
    """
    A general-purpose HTTP load testing and benchmarking library.
    """

    def __init__(self, url, num_requests, concurrency=1, request_type="GET", data=None):
        """
        Initialize the HTTPLoadTest object.

        Args:
            url (str): The URL to send requests to.
            num_requests (int): The total number of requests to send.
            concurrency (int, optional): The number of concurrent requests to send. Defaults to 1.
            request_type (str, optional): The type of HTTP request to send (GET, POST, etc.). Defaults to "GET".
            data (dict, optional): Data to send with a POST request. Defaults to None.
        """
        self.url = url
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.request_type = request_type.upper()
        self.data = data
        self.latencies = []
        self.errors = 0

        self.average_latency = None
        self.total_time = None
        self.percentile_50th = None
        self.percentile_75th = None
        self.percentile_95th = None
        self.percentile_99th = None
        self.percentiles = {}


    def run_test(self):
        """
        Runs the load test and prints results.
        """
        start_time = time.time()
        self._send_requests()
        end_time = time.time()

        self.total_time = end_time - start_time
        self.average_latency = self.get_average_latency()

        percentiles = [50, 75, 95, 99]
        latency_percentiles = self._calculate_percentiles(percentiles)
        print(f"Total Requests: {self.num_requests}")
        print(f"Concurrency: {self.concurrency}")
        print(f"Errors: {self.errors}")
        print(f"Total Time: {self.total_time:.4f} seconds")
        print(f"Average Latency: {self.average_latency:.4f} seconds")
        print(f"Percentiles:")
        for percentile, latency in zip(percentiles, latency_percentiles):
            self.percentiles["percentile_" + str(percentile) + "th"] = latency
            print(f"  - {percentile}%: {latency:.4f} seconds")

    def _send_requests(self):
        """
        Sends the specified number of requests concurrently.
        """
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = []
            for _ in range(self.num_requests):
                future = executor.submit(self._send_request)
                futures.append(future)

            for future in futures:
                try:
                    latency = future.result()
                    self.latencies.append(latency)
                except Exception as e:
                    self.errors += 1
                    print(f"Error: {e}")

    def _send_request(self):
        """
        Sends a single request and measures the latency.
        """
        start_time = time.time()
        if self.request_type == "GET":
            response = requests.get(self.url)
        elif self.request_type == "POST":
            response = requests.post(self.url, json=self.data)
        else:
            raise ValueError(f"Unsupported request type: {self.request_type}")
        response.raise_for_status()  # Raise error for non-2xx response codes
        end_time = time.time()
        return end_time - start_time

    def get_average_latency(self):
        """
        Calculates the average latency of all requests.
        """
        if not self.latencies:
            return 0.0
        return sum(self.latencies) / len(self.latencies)

    def _calculate_percentiles(self, percentiles):
        """
        Calculates the percentiles of the recorded latencies.
        """
        return np.percentile(self.latencies, percentiles)


# Local testing
if __name__ == "__main__":
    test = HTTPLoadTest(url="https://www.google.com", num_requests=100, concurrency=4, request_type="GET")
    test.run_test()