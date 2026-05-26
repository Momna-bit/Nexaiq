"""
NexaIQ Pipeline Scheduler
Runs the DAG on a schedule — like Airflow Scheduler
"""
import time
import datetime
import requests
import json
from nexaiq_pipeline import create_nexaiq_dag

def get_token():
    """Get fresh auth token"""
    try:
        res = requests.post(
            "http://127.0.0.1:8001/auth/login",
            data={"username": "test@nexaiq.com", "password": "test123"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=10
        )
        return res.json().get("access_token")
    except:
        return None

def run_scheduled_pipeline():
    """Run pipeline with auth token"""
    print(f"\n[Scheduler] Triggering pipeline at {datetime.datetime.now()}")
    token = get_token()
    dag = create_nexaiq_dag()
    results = dag.run(context={
        "dataset_id": f"scheduled-{datetime.datetime.now().strftime('%Y%m%d%H%M')}",
        "org_id": "e22043da-16d5-49b9-b6da-5765a5e7edd9",
        "token": token
    })
    print(f"[Scheduler] Pipeline complete: {json.dumps(results.get('task_send_completion_report', {}), indent=2)}")
    return results

def start_scheduler(interval_seconds: int = 3600):
    """
    Start the scheduler — runs pipeline every interval_seconds
    Default: every hour (3600 seconds)
    Like Airflow scheduler
    """
    print(f"[Scheduler] Starting NexaIQ Pipeline Scheduler")
    print(f"[Scheduler] Schedule: every {interval_seconds} seconds")
    print(f"[Scheduler] Press Ctrl+C to stop\n")

    run_count = 0
    while True:
        run_count += 1
        print(f"[Scheduler] Run #{run_count}")
        try:
            run_scheduled_pipeline()
        except Exception as e:
            print(f"[Scheduler] Pipeline failed: {e}")
        print(f"[Scheduler] Next run in {interval_seconds} seconds...")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # Run once immediately for demo
    run_scheduled_pipeline()
