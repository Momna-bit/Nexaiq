"""
NexaIQ Kafka Consumer
Listens to events and triggers actions
"""

from events import NexaIQConsumer, KafkaMessage
from producer import producer, on_file_uploaded, on_pipeline_completed
from producer import on_model_trained, on_anomaly_detected
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../airflow_dags'))

def handle_file_uploaded(message: KafkaMessage):
    """When file uploaded → trigger pipeline DAG"""
    data = message.value
    print(f"\n  [Handler] File uploaded: {data['filename']}")
    print(f"  [Handler] Triggering Airflow DAG for dataset: {data['dataset_id']}")
    try:
        from nexaiq_pipeline import create_nexaiq_dag
        dag = create_nexaiq_dag()
        dag.run(context={
            "dataset_id": data["dataset_id"],
            "org_id": data["org_id"]
        })
    except Exception as e:
        print(f"  [Handler] DAG trigger failed: {e}")

def handle_pipeline_completed(message: KafkaMessage):
    """When pipeline completes → log success"""
    data = message.value
    print(f"\n  [Handler] Pipeline complete for: {data['dataset_id']}")
    print(f"  [Handler] Results: {data['results']}")

def handle_model_trained(message: KafkaMessage):
    """When model trained → log best model"""
    data = message.value
    print(f"\n  [Handler] Model trained: {data['best_model']}")
    print(f"  [Handler] Score: {data['best_score']*100:.1f}%")

def handle_anomaly_detected(message: KafkaMessage):
    """When anomaly detected → log alert"""
    data = message.value
    print(f"\n  [Handler] ANOMALY ALERT!")
    print(f"  [Handler] Count: {data['anomaly_count']}")
    print(f"  [Handler] AI Alert: {data['ai_alert']}")

if __name__ == "__main__":
    print("Starting NexaIQ Kafka Consumer...\n")

    # Create consumer
    consumer = NexaIQConsumer(
        topics=["file.uploaded", "pipeline.completed",
                "model.trained", "anomaly.detected"],
        group_id="nexaiq-pipeline-group"
    )

    # Subscribe handlers
    consumer.subscribe("file.uploaded", handle_file_uploaded)
    consumer.subscribe("pipeline.completed", handle_pipeline_completed)
    consumer.subscribe("model.trained", handle_model_trained)
    consumer.subscribe("anomaly.detected", handle_anomaly_detected)

    print("\nProducing test events...")
    on_file_uploaded(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        dataset_id="kafka-stream-001",
        filename="sales_data.csv",
        blob_url="https://nexaiqstorage.blob.core.windows.net/test.csv"
    )
    on_model_trained(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        best_model="XGBoost",
        best_score=0.94
    )
    on_anomaly_detected(
        org_id="e22043da-16d5-49b9-b6da-5765a5e7edd9",
        anomalies=[{"column": "revenue", "value": 250000}],
        ai_alert="EU revenue spike detected — immediate attention required."
    )

    print("\nConsuming events...")
    consumer.consume_all(producer)
    print("\nAll events consumed successfully!")
