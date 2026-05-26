"""
NexaIQ Monitoring Service
Exposes Prometheus metrics endpoint
Simulates Grafana dashboard data
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
import time
import datetime
from metrics import (
    track_request, track_error, track_ml_training,
    track_anomaly, track_file_upload, set_services_up,
    get_metrics
)

app = FastAPI(title="NexaIQ Monitoring Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "auth": "http://127.0.0.1:8001",
    "ingestion": "http://127.0.0.1:8002",
    "ml": "http://127.0.0.1:8003",
    "alerts": "http://127.0.0.1:8004",
    "query": "http://127.0.0.1:8005"
}

def check_services() -> dict:
    """Check which services are running"""
    status = {}
    up_count = 0
    for name, url in SERVICES.items():
        try:
            res = requests.get(f"{url}/", timeout=2)
            status[name] = {
                "status": "up" if res.status_code == 200 else "degraded",
                "response_time_ms": res.elapsed.total_seconds() * 1000,
                "url": url
            }
            if res.status_code == 200:
                up_count += 1
                track_request(name, "/", "GET", 200)
        except Exception as e:
            status[name] = {
                "status": "down",
                "response_time_ms": 0,
                "url": url,
                "error": str(e)
            }
            track_error(name, "connection_failed")
    set_services_up(up_count)
    return status

@app.get("/")
def root():
    return {"message": "NexaIQ Monitoring Service running"}

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    """Prometheus metrics endpoint — scraped by Prometheus"""
    check_services()
    return get_metrics()

@app.get("/health")
def health():
    """Health check — like Grafana health endpoint"""
    services = check_services()
    up = sum(1 for s in services.values() if s["status"] == "up")
    return {
        "status": "healthy" if up >= 3 else "degraded",
        "services_up": up,
        "services_total": len(SERVICES),
        "services": services,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/dashboard")
def dashboard():
    """Summary dashboard data — like Grafana panels"""
    services = check_services()

    # Simulate tracking some metrics
    track_file_upload("e22043da-16d5-49b9-b6da-5765a5e7edd9")
    track_ml_training(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        model_name="LogisticRegression",
        duration=15.2,
        accuracy=1.0
    )
    track_anomaly("e22043da-16d5-49b9-b6da-5765a5e7edd9", "revenue")

    return {
        "services": services,
        "metrics_summary": {
            "total_services": len(SERVICES),
            "services_up": sum(1 for s in services.values() if s["status"] == "up"),
            "avg_response_time_ms": sum(
                s["response_time_ms"] for s in services.values()
            ) / len(SERVICES)
        },
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
