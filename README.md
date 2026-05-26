# NexaIQ — B2B AI Decision Intelligence Platform

<div align="center">

**Palantir for mid-market companies.**
Upload your data. Get autonomous AI-powered decisions.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Azure](https://img.shields.io/badge/Azure-Blob_Storage-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white)](https://mongodb.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![MLflow](https://img.shields.io/badge/MLflow-2.7-0194E2?style=flat-square&logo=mlflow&logoColor=white)](https://mlflow.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## What is NexaIQ?

NexaIQ is a **production-grade B2B SaaS platform** that transforms raw business data into autonomous AI-driven decisions. Upload a CSV file and the platform automatically ingests, transforms, trains ML models, detects anomalies, and delivers executive alerts — no data team required.

---

## Architecture
CSV Upload → Azure Blob Storage → Kafka Event
↓
Airflow DAG → DBT RAW→CLEAN→MART
↓
AutoML (XGBoost / LightGBM / RandomForest) + MLflow
↓
Anomaly Detection → LangGraph Agents → Executive Report
↓
RAG Pipeline (ChromaDB) → Ask Your Data
↓
Prometheus + Grafana Monitoring across 7 services

---

## Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | FastAPI · Python 3.11 · PostgreSQL · MongoDB Atlas |
| **Data Pipeline** | Apache Airflow · DBT · Apache Kafka |
| **ML / MLOps** | XGBoost · LightGBM · RandomForest · MLflow · Evidently AI |
| **GenAI & Agents** | OpenAI API · LangGraph · ChromaDB · RAG Pipeline |
| **Frontend** | React 18 · TypeScript · Tailwind CSS · Recharts · Zustand |
| **Cloud** | Azure Blob Storage · Azure Container Apps |
| **Infrastructure** | Docker · Kubernetes · GitHub Actions |
| **Monitoring** | Prometheus · Grafana · Health Checks |

---

## Services

| Service | Port | Description |
|---|---|---|
| Auth Service | `8001` | JWT authentication · Multi-tenant RBAC |
| Ingestion Service | `8002` | CSV upload · Azure Blob · DBT pipeline |
| ML Service | `8003` | AutoML engine · MLflow tracking |
| Alert Service | `8004` | Anomaly detection · GPT executive alerts |
| Query Service | `8005` | Text-to-SQL · Plain English to results |
| Monitoring Service | `8006` | Prometheus metrics · Service health |
| RAG Service | `8007` | ChromaDB · Document Q&A |
| MLflow UI | `5000` | Experiment tracking · Model registry |

---

## Key Features

### Multi-Tenant SaaS Architecture
Every organisation gets isolated data scoped by `org_id`. Admin, Analyst, and Viewer roles enforced with JWT auth.

### Azure Blob Storage + Event-Driven Pipeline
Every CSV upload goes to Azure Blob in an org-isolated container. A Kafka `file.uploaded` event fires automatically triggering the Airflow DAG.

### Apache Airflow DAG Orchestration
5-task DAG runs automatically: `validate → run_pipeline → train_models → detect_anomalies → send_report`.

### DBT Data Models
Staging and mart models transform RAW → CLEAN → MART with automated data tests and auto-generated lineage documentation.

### AutoML Engine + MLflow
Trains XGBoost, LightGBM, RandomForest, and LogisticRegression simultaneously. Selects the best model. Every experiment logged to MLflow.

### Anomaly Detection + GenAI Alerts
Z-score and IQR anomaly detection on every dataset. GPT-3.5 writes natural language executive alerts automatically.

### Text-to-SQL Interface
Plain English question → LLM generates SQL → runs against PostgreSQL → returns structured results.

### RAG Pipeline (ChromaDB)
Documents chunked and embedded into ChromaDB. Semantic search retrieves context. GPT answers grounded in your documents with source attribution.

### LangGraph Autonomous Agents
4 agents in sequence: **Analyst** → **Report Writer** → **Critic** (8/10 quality score) → **Action**. No human needed.

### Prometheus + Grafana Monitoring
Prometheus metrics — request counts, error rates, response times, ML accuracy across all 7 services.

---

## Project Structure
nexaiq/
├── backend/
│   ├── auth_service/          # JWT + RBAC (port 8001)
│   ├── ingestion_service/     # Azure Blob + pipeline (port 8002)
│   ├── ml_service/            # AutoML + MLflow (port 8003)
│   ├── alert_service/         # Anomaly + GenAI (port 8004)
│   └── query_service/         # Text-to-SQL (port 8005)
├── airflow_dags/              # Pipeline DAG + scheduler
├── agents/                    # LangGraph autonomous agents
├── docker/                    # Dockerfiles for all services
├── frontend/                  # React + TypeScript dashboard
├── k8s/                       # Kubernetes deployment configs
├── kafka/                     # Kafka producer + consumer
├── mongodb/                   # MongoDB client + log service
├── monitoring/                # Prometheus metrics (port 8006)
├── nexaiq_dbt/                # DBT staging + mart models
├── rag/                       # ChromaDB + RAG pipeline (port 8007)
├── docker-compose.yml
├── start.sh
└── .env.example

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Momna-bit/Nexaiq.git
cd Nexaiq

# Set up environment
cp .env.example .env
# Fill in your API keys in .env

# Install Python dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose bcrypt \
  azure-storage-blob openai scikit-learn xgboost lightgbm mlflow \
  pandas pymongo chromadb langchain langgraph prometheus-client \
  dbt-core dbt-postgres kafka-python

# Install frontend
cd frontend && npm install && cd ..

# Start all services
bash start.sh

# Start frontend (new terminal)
cd frontend && npm run dev
```

---

## Data Pipeline Flow

User uploads CSV via React dashboard
FastAPI saves to Azure Blob Storage (org-isolated container)
Kafka producer fires file.uploaded event
Kafka consumer triggers Airflow DAG automatically
DAG runs 5 tasks in sequence:

Validate input
DBT RAW → CLEAN → MART transformation
AutoML trains 4 models → best selected → MLflow logged
Anomaly detection → GPT writes executive alert
Completion report dispatched


Results visible in React dashboard
Ask questions in plain English via Text-to-SQL
Query documents via RAG pipeline
LangGraph agents investigate anomalies autonomously


---

## API Reference

### Auth (`:8001`)
POST /auth/register   Register org + admin user
POST /auth/login      Login and get JWT token
GET  /auth/me         Get current user info

### ML (`:8003`)
POST /train           Run AutoML on dataset
GET  /models          List all trained models

### Alerts (`:8004`)
POST /detect-anomalies    Run detection + generate AI alert
POST /ml-insight          Generate business summary of ML results

### Query (`:8005`)
POST /ask             Natural language to SQL to results
GET  /schema          List available tables and datasets

### RAG (`:8007`)
POST /ingest          Add document to ChromaDB vector store
POST /ask             Ask question grounded in documents
GET  /stats           Vector store statistics

---

## Environment Variables

```bash
DATABASE_URL=postgresql://postgres:password@localhost:5432/nexaiq_db
SECRET_KEY=your-secret-key-here
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER=datasets
OPENAI_API_KEY=sk-...
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

---

## Deployment

### Docker Compose
```bash
docker-compose up --build
```

### Kubernetes
```bash
kubectl apply -f k8s/secrets.yml
kubectl apply -f k8s/deployment.yml
```

### Azure Container Apps
```bash
az containerapp up --name nexaiq \
  --resource-group nexaiq-rg \
  --image nexaiq/auth-service:latest
```

---

## What I Learned

- Microservices architecture with 7 independent services
- Event-driven design with Kafka decoupling services
- MLOps in practice — MLflow experiment tracking and model versioning
- RAG pipeline — chunking, vector similarity search, grounded generation
- Multi-agent systems with LangGraph orchestration
- Production monitoring with Prometheus metrics
- Multi-tenancy with org-scoped data isolation
- Modern data stack — DBT models, lineage graphs, data tests

---

## Built By

**Momna Ali** — Data Engineer and ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/momna-ali)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-6d28d9?style=flat-square)](https://momna-bit.github.io)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/Momna-bit)

---

<div align="center">
  <sub>Python · FastAPI · React · Azure · MLflow · LangGraph · ChromaDB · Kafka · DBT · Airflow · Prometheus</sub>
</div>
