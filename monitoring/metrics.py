from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
import time

registry = CollectorRegistry()

REQUEST_COUNT = Counter('nexaiq_requests_total', 'Total requests', ['service', 'endpoint', 'method', 'status'], registry=registry)
ERROR_COUNT = Counter('nexaiq_errors_total', 'Total errors', ['service', 'error_type'], registry=registry)
ML_TRAINING_COUNT = Counter('nexaiq_ml_training_total', 'Total ML runs', ['org_id', 'model_name'], registry=registry)
ANOMALY_COUNT = Counter('nexaiq_anomalies_total', 'Total anomalies', ['org_id', 'column_name'], registry=registry)
FILE_UPLOAD_COUNT = Counter('nexaiq_file_uploads_total', 'Total uploads', ['org_id'], registry=registry)

REQUEST_DURATION = Histogram('nexaiq_request_duration_seconds', 'Request duration', ['service', 'endpoint'], buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0], registry=registry)
ML_TRAINING_DURATION = Histogram('nexaiq_ml_training_duration_seconds', 'Training duration', ['model_name'], buckets=[1, 5, 10, 30, 60, 120, 300], registry=registry)

SERVICES_UP = Gauge('nexaiq_services_up', 'Services running', registry=registry)
MODEL_ACCURACY = Gauge('nexaiq_model_accuracy', 'Model accuracy', ['org_id', 'model_name'], registry=registry)
DATASET_ROWS = Gauge('nexaiq_dataset_rows', 'Dataset rows', ['org_id', 'dataset_id'], registry=registry)

def track_request(service, endpoint, method, status):
    REQUEST_COUNT.labels(service=service, endpoint=endpoint, method=method, status=str(status)).inc()

def track_error(service, error_type):
    ERROR_COUNT.labels(service=service, error_type=error_type).inc()

def track_ml_training(org_id, model_name, duration, accuracy):
    ML_TRAINING_COUNT.labels(org_id=org_id[:8], model_name=model_name).inc()
    ML_TRAINING_DURATION.labels(model_name=model_name).observe(duration)
    MODEL_ACCURACY.labels(org_id=org_id[:8], model_name=model_name).set(accuracy)

def track_anomaly(org_id, column_name):
    ANOMALY_COUNT.labels(org_id=org_id[:8], column_name=column_name).inc()

def track_file_upload(org_id):
    FILE_UPLOAD_COUNT.labels(org_id=org_id[:8]).inc()

def set_services_up(count):
    SERVICES_UP.set(count)

def get_metrics():
    return generate_latest(registry).decode('utf-8')
