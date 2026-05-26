#!/bin/bash
echo "🚀 Starting NexaIQ Services..."

# Start Auth Service
cd ~/nexaiq/backend/auth_service
uvicorn main:app --port 8001 &
echo "✅ Auth Service started on port 8001"

# Start Ingestion Service
cd ~/nexaiq/backend/ingestion_service
uvicorn main:app --port 8002 &
echo "✅ Ingestion Service started on port 8002"

# Start ML Service
cd ~/nexaiq/backend/ml_service
uvicorn main:app --port 8003 &
echo "✅ ML Service started on port 8003"

# Start Alert Service
cd ~/nexaiq/backend/alert_service
uvicorn main:app --port 8004 &
echo "✅ Alert Service started on port 8004"

# Start Query Service
cd ~/nexaiq/backend/query_service
uvicorn main:app --port 8005 &
echo "✅ Query Service started on port 8005"
cd C:/Users/User/nexaiq/airflow_dags
python scheduler.py &
echo "✅ Pipeline Scheduler started"
# Start MLflow
cd ~/nexaiq
mlflow server --host 127.0.0.1 --port 5000 &
echo "✅ MLflow started on port 5000"

echo ""
echo "🎉 All services running!"
echo "Auth:      http://127.0.0.1:8001"
echo "Ingestion: http://127.0.0.1:8002"
echo "ML:        http://127.0.0.1:8003"
echo "Alerts:    http://127.0.0.1:8004"
echo "Query:     http://127.0.0.1:8005"
echo "MLflow:    http://127.0.0.1:5000"
