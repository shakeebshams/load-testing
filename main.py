import requests
from flask import Flask, request, jsonify
from HTTPLoadTest import HTTPLoadTest

app = Flask(__name__)

@app.route("/run_load_test", methods=["POST"])
def run_load_test():
    data = request.get_json()
    print(data)
    test = HTTPLoadTest(**data)
    test.run_test()
    return jsonify({
        "total_requests": test.num_requests,
        "concurrency": test.concurrency,
        "errors": test.errors,
        "total_time": test.total_time,
        "average_latency": test.average_latency,
        "percentiles": test.percentiles,
    })

if __name__ == "__main__":
    app.run(debug=True)  # Set debug=False for production