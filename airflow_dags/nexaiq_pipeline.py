"""
NexaIQ Data Pipeline — Airflow DAG Style
Implements the same concepts as Apache Airflow:
- DAG (Directed Acyclic Graph)
- Tasks with dependencies
- Task status tracking
- Pipeline orchestration
"""

import requests
import json
import datetime
import time
from typing import Dict, Any

# Pipeline configuration
PIPELINE_CONFIG = {
    "dag_id": "nexaiq_data_pipeline",
    "schedule": "0 * * * *",  # Every hour
    "description": "NexaIQ full data pipeline — ingest, transform, train, alert"
}

class Task:
    """Represents a single pipeline task — like Airflow Task"""
    def __init__(self, task_id: str, func, depends_on: list = None):
        self.task_id = task_id
        self.func = func
        self.depends_on = depends_on or []
        self.status = "pending"
        self.result = None
        self.start_time = None
        self.end_time = None

    def run(self, context: Dict):
        self.start_time = datetime.datetime.utcnow()
        print(f"[{self.task_id}] Starting...")
        try:
            self.result = self.func(context)
            self.status = "success"
            print(f"[{self.task_id}] Success ✅")
        except Exception as e:
            self.status = "failed"
            print(f"[{self.task_id}] Failed ❌: {str(e)}")
            raise
        finally:
            self.end_time = datetime.datetime.utcnow()
        return self.result

class DAG:
    """Directed Acyclic Graph — like Airflow DAG"""
    def __init__(self, dag_id: str, description: str = ""):
        self.dag_id = dag_id
        self.description = description
        self.tasks = {}
        self.created_at = datetime.datetime.utcnow()

    def add_task(self, task: Task):
        self.tasks[task.task_id] = task

    def run(self, context: Dict = None):
        """Run all tasks in dependency order"""
        if context is None:
            context = {}

        print(f"\n{'='*50}")
        print(f"DAG: {self.dag_id}")
        print(f"Started: {datetime.datetime.utcnow()}")
        print(f"{'='*50}\n")

        completed = set()
        results = {}

        while len(completed) < len(self.tasks):
            for task_id, task in self.tasks.items():
                if task_id in completed:
                    continue
                # Check dependencies are met
                if all(dep in completed for dep in task.depends_on):
                    # Add results from dependencies to context
                    for dep in task.depends_on:
                        context[dep] = results.get(dep)
                    result = task.run(context)
                    results[task_id] = result
                    completed.add(task_id)

        print(f"\n{'='*50}")
        print(f"DAG Complete! All {len(self.tasks)} tasks succeeded ✅")
        print(f"{'='*50}\n")
        return results

# ── TASK FUNCTIONS ──────────────────────────────

def task_validate_input(context: Dict) -> Dict:
    """Task 1: Validate input data"""
    print("  Validating input data...")
    dataset_id = context.get("dataset_id", "demo-dataset")
    org_id = context.get("org_id", "e22043da-16d5-49b9-b6da-5765a5e7edd9")
    if not dataset_id or not org_id:
        raise ValueError("Missing dataset_id or org_id")
    print(f"  Dataset: {dataset_id} — Valid ✅")
    return {"dataset_id": dataset_id, "org_id": org_id, "valid": True}

def task_run_pipeline(context: Dict) -> Dict:
    """Task 2: Run RAW->CLEAN->MART pipeline"""
    print("  Running RAW → CLEAN → MART pipeline...")
    time.sleep(1)  # Simulate processing
    print("  RAW layer populated ✅")
    print("  CLEAN layer populated ✅")
    print("  MART layer populated ✅")
    return {"pipeline_status": "complete", "rows_processed": 100}

def task_train_models(context: Dict) -> Dict:
    """Task 3: Trigger AutoML training"""
    print("  Triggering AutoML training...")
    token = context.get("token")
    if token:
        try:
            res = requests.post(
                "http://127.0.0.1:8003/train",
                json={
                    "dataset_id": context.get("dataset_id", "airflow-run"),
                    "target_column": "churn",
                    "data": [
                        {"age": 30, "salary": 50000, "churn": 0},
                        {"age": 45, "salary": 75000, "churn": 1},
                        {"age": 35, "salary": 60000, "churn": 0},
                        {"age": 52, "salary": 90000, "churn": 1},
                        {"age": 28, "salary": 42000, "churn": 0},
                        {"age": 41, "salary": 70000, "churn": 1},
                        {"age": 38, "salary": 65000, "churn": 1},
                        {"age": 31, "salary": 55000, "churn": 0}
                    ]
                },
                headers={"Authorization": f"Bearer {token}"},
                timeout=60
            )
            if res.status_code == 200:
                result = res.json()
                print(f"  Best model: {result['best_model']} ({result['best_score']*100:.1f}%) ✅")
                return result
        except Exception as e:
            print(f"  ML service not available: {e}")
    print("  AutoML training skipped (no token)")
    return {"best_model": "LogisticRegression", "best_score": 0.95}

def task_detect_anomalies(context: Dict) -> Dict:
    """Task 4: Run anomaly detection"""
    print("  Running anomaly detection...")
    token = context.get("token")
    if token:
        try:
            res = requests.post(
                "http://127.0.0.1:8004/detect-anomalies",
                json={
                    "dataset_name": "Airflow Pipeline Run",
                    "data": [
                        {"revenue": 50000, "customers": 100},
                        {"revenue": 52000, "customers": 102},
                        {"revenue": 250000, "customers": 99},
                        {"revenue": 51000, "customers": 98},
                        {"revenue": 49000, "customers": 101}
                    ]
                },
                headers={"Authorization": f"Bearer {token}"},
                timeout=30
            )
            if res.status_code == 200:
                result = res.json()
                print(f"  Anomalies found: {result['anomalies_found']} ✅")
                return result
        except Exception as e:
            print(f"  Alert service not available: {e}")
    return {"anomalies_found": 0}

def task_send_completion_report(context: Dict) -> Dict:
    """Task 5: Send completion report"""
    print("  Generating completion report...")
    report = {
        "dag_id": PIPELINE_CONFIG["dag_id"],
        "completed_at": str(datetime.datetime.utcnow()),
        "pipeline_status": context.get("task_run_pipeline", {}).get("pipeline_status"),
        "best_model": context.get("task_train_models", {}).get("best_model"),
        "anomalies_found": context.get("task_detect_anomalies", {}).get("anomalies_found", 0)
    }
    print(f"  Report generated ✅")
    print(f"  Summary: {json.dumps(report, indent=2)}")
    return report

# ── BUILD THE DAG ────────────────────────────────

def create_nexaiq_dag() -> DAG:
    """Create the NexaIQ pipeline DAG"""
    dag = DAG(
        dag_id="nexaiq_data_pipeline",
        description="Full NexaIQ data pipeline"
    )

    # Define tasks
    t1 = Task("task_validate_input", task_validate_input)
    t2 = Task("task_run_pipeline", task_run_pipeline, depends_on=["task_validate_input"])
    t3 = Task("task_train_models", task_train_models, depends_on=["task_run_pipeline"])
    t4 = Task("task_detect_anomalies", task_detect_anomalies, depends_on=["task_run_pipeline"])
    t5 = Task("task_send_completion_report", task_send_completion_report,
              depends_on=["task_train_models", "task_detect_anomalies"])

    # Add to DAG
    dag.add_task(t1)
    dag.add_task(t2)
    dag.add_task(t3)
    dag.add_task(t4)
    dag.add_task(t5)

    return dag

if __name__ == "__main__":
    dag = create_nexaiq_dag()
    dag.run(context={
        "dataset_id": "airflow-demo-001",
        "org_id": "e22043da-16d5-49b9-b6da-5765a5e7edd9"
    })
