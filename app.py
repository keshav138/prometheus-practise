from flask import Flask,request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

REQUEST_COUNT = Counter(
    'flask_request_count', # variable id for grafana
    'Total request count', # descripton
    ['method', 'endpoint','status']
)

REQUEST_LATENCY = Histogram(
    'flask_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

@app.before_request
def start_timer():
    request._start_time = time.time()

@app.after_request
def record_metrics(response):
    latency = time.time() - request._start_time
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    REQUEST_COUNT.labels(method=request.method,endpoint=request.path,status=response.status_code).inc()
    return response

@app.route('/')
def index():
    return "Hello from flask"

@app.route('/data')
def data():
    return {'message' : 'something', 'status' : 'ok'}

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
