"""
NexaIQ Kafka Producer
Fires events when things happen in the platform
"""

from events import NexaIQProducer, publish_event
import datetime

# Global producer instance
producer = NexaIQProducer(broker="localhost:9092")

def on_file_uploaded(org_id: str, dataset_id: str, filename: str, blob_url: str):
    """Fire event when file is uploaded to Azure Blob"""
    event_data = {
        "org_id": org_id,
        "dataset_id": dataset_id,
        "filename": filename,
        "blob_url": blob_url,
        "uploaded_at": datetime.datetime.utcnow().isoformat()
    }
    msg = producer.produce(
        topic="file.uploaded",
        key=dataset_id,
        value=event_data
    )
    producer.flush()
    return msg

def on_pipeline_completed(org_id: str, dataset_id: str, results: dict):
    """Fire event when pipeline completes"""
    event_data = {
        "org_id": org_id,
        "dataset_id": dataset_id,
        "results": results,
        "completed_at": datetime.datetime.utcnow().isoformat()
    }
    msg = producer.produce(
        topic="pipeline.completed",
        key=dataset_id,
        value=event_data
    )
    producer.flush()
    return msg

def on_model_trained(org_id: str, best_model: str, best_score: float):
    """Fire event when model is trained"""
    event_data = {
        "org_id": org_id,
        "best_model": best_model,
        "best_score": best_score,
        "trained_at": datetime.datetime.utcnow().isoformat()
    }
    msg = producer.produce(
        topic="model.trained",
        key=org_id,
        value=event_data
    )
    producer.flush()
    return msg

def on_anomaly_detected(org_id: str, anomalies: list, ai_alert: str):
    """Fire event when anomaly is detected"""
    event_data = {
        "org_id": org_id,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies,
        "ai_alert": ai_alert,
        "detected_at": datetime.datetime.utcnow().isoformat()
    }
    msg = producer.produce(
        topic="anomaly.detected",
        key=org_id,
        value=event_data
    )
    producer.flush()
    return msg

if __name__ == "__main__":
    print("Testing NexaIQ Kafka Producer...\n")

    # Simulate events
    print("1. File uploaded event:")
    on_file_uploaded(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        dataset_id="dataset-kafka-001",
        filename="revenue_data.csv",
        blob_url="https://nexaiqstorage.blob.core.windows.net/org-xxx/revenue_data.csv"
    )

    print("\n2. Pipeline completed event:")
    on_pipeline_completed(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        dataset_id="dataset-kafka-001",
        results={"rows_processed": 1000, "status": "complete"}
    )

    print("\n3. Model trained event:")
    on_model_trained(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        best_model="XGBoost",
        best_score=0.94
    )

    print("\n4. Anomaly detected event:")
    on_anomaly_detected(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        anomalies=[{"column": "revenue", "value": 250000, "z_score": 2.65}],
        ai_alert="Revenue spike detected in EU region."
    )

    print("\nAll events produced successfully!")
    print(f"Messages in file.uploaded: {len(producer.get_messages('file.uploaded'))}")
    print(f"Messages in pipeline.completed: {len(producer.get_messages('pipeline.completed'))}")
    print(f"Messages in model.trained: {len(producer.get_messages('model.trained'))}")
    print(f"Messages in anomaly.detected: {len(producer.get_messages('anomaly.detected'))}")
