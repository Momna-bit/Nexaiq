"""
NexaIQ Log Service — MongoDB
Stores all unstructured data: logs, alerts, agent outputs, events
"""

from mongo_client import get_db
import datetime
import uuid

def log_pipeline_run(org_id: str, dataset_id: str, results: dict):
    """Log a pipeline run to MongoDB"""
    db = get_db()
    doc = {
        "_id": str(uuid.uuid4()),
        "type": "pipeline_run",
        "org_id": org_id,
        "dataset_id": dataset_id,
        "results": results,
        "created_at": datetime.datetime.utcnow()
    }
    db.pipeline_logs.insert_one(doc)
    print(f"Pipeline log saved to MongoDB: {doc['_id']}")
    return doc["_id"]

def log_anomaly_alert(org_id: str, anomalies: list, ai_alert: str):
    """Log anomaly alert to MongoDB"""
    db = get_db()
    doc = {
        "_id": str(uuid.uuid4()),
        "type": "anomaly_alert",
        "org_id": org_id,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "ai_alert": ai_alert,
        "created_at": datetime.datetime.utcnow()
    }
    db.alerts.insert_one(doc)
    print(f"Alert saved to MongoDB: {doc['_id']}")
    return doc["_id"]

def log_ml_training(org_id: str, best_model: str, best_score: float, all_results: list):
    """Log ML training results to MongoDB"""
    db = get_db()
    doc = {
        "_id": str(uuid.uuid4()),
        "type": "ml_training",
        "org_id": org_id,
        "best_model": best_model,
        "best_score": best_score,
        "all_results": all_results,
        "created_at": datetime.datetime.utcnow()
    }
    db.ml_logs.insert_one(doc)
    print(f"ML training log saved to MongoDB: {doc['_id']}")
    return doc["_id"]

def log_query(org_id: str, question: str, sql: str, row_count: int):
    """Log text-to-SQL query to MongoDB"""
    db = get_db()
    doc = {
        "_id": str(uuid.uuid4()),
        "type": "query",
        "org_id": org_id,
        "question": question,
        "generated_sql": sql,
        "row_count": row_count,
        "created_at": datetime.datetime.utcnow()
    }
    db.query_logs.insert_one(doc)
    print(f"Query log saved to MongoDB: {doc['_id']}")
    return doc["_id"]

def get_recent_alerts(org_id: str, limit: int = 10) -> list:
    """Get recent alerts for an org"""
    db = get_db()
    alerts = list(db.alerts.find(
        {"org_id": org_id},
        sort=[("created_at", -1)],
        limit=limit
    ))
    for a in alerts:
        a["created_at"] = str(a["created_at"])
    return alerts

def get_pipeline_history(org_id: str, limit: int = 10) -> list:
    """Get pipeline run history"""
    db = get_db()
    logs = list(db.pipeline_logs.find(
        {"org_id": org_id},
        sort=[("created_at", -1)],
        limit=limit
    ))
    for l in logs:
        l["created_at"] = str(l["created_at"])
    return logs

if __name__ == "__main__":
    ORG_ID = "e22043da-16d5-49b9-b6da-5765a5e7edd9"

    print("Testing MongoDB Log Service...\n")

    # Test pipeline log
    log_id = log_pipeline_run(
        org_id=ORG_ID,
        dataset_id="test-dataset-001",
        results={"rows_processed": 100, "status": "complete", "duration_seconds": 15}
    )

    # Test anomaly alert log
    log_id = log_anomaly_alert(
        org_id=ORG_ID,
        anomalies=[{"column": "revenue", "value": 250000, "z_score": 2.65}],
        ai_alert="Revenue spike detected in EU region. Immediate attention required."
    )

    # Test ML training log
    log_id = log_ml_training(
        org_id=ORG_ID,
        best_model="LogisticRegression",
        best_score=1.0,
        all_results=[
            {"model": "LogisticRegression", "accuracy": 1.0},
            {"model": "RandomForest", "accuracy": 1.0},
            {"model": "XGBoost", "accuracy": 0.0}
        ]
    )

    # Test query log
    log_id = log_query(
        org_id=ORG_ID,
        question="Show me all datasets",
        sql="SELECT * FROM datasets WHERE org_id = 'xxx'",
        row_count=5
    )

    # Test retrieval
    print("\nRecent alerts from MongoDB:")
    alerts = get_recent_alerts(ORG_ID)
    for a in alerts:
        print(f"  - {a['type']}: {a['ai_alert'][:50]}...")

    print("\nPipeline history from MongoDB:")
    history = get_pipeline_history(ORG_ID)
    for h in history:
        print(f"  - {h['type']}: {h['results']}")

    print("\nAll MongoDB tests passed!")
