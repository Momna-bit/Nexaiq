# NexaIQ — B2B AI Decision Intelligence Platform

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

**Palantir for mid-market companies. Upload your data. Get autonomous AI-powered decisions.**

[Live Demo](#) · [Architecture](#architecture) · [Tech Stack](#tech-stack) · [Quick Start](#quick-start) · [Built By](#built-by)

---

## The Problem NexaIQ Solves

Most mid-market companies are sitting on enormous amounts of business data — sales records, customer behaviour, revenue trends, operational metrics — but have no practical way to act on it in real time.

Hiring a full data team costs hundreds of thousands of dollars per year. Enterprise tools like Palantir or Databricks cost millions in licensing fees. Small BI tools like Power BI or Tableau show charts, but they do not think for you — someone still has to interpret the data, build the models, detect the anomalies, and write the reports.

**NexaIQ eliminates that gap.**

It is a fully autonomous B2B SaaS platform that acts as an entire data team in software. Upload a CSV. The platform does everything else — ingestion, transformation, ML training, anomaly detection, executive reporting, and intelligent Q&A — automatically, with zero manual intervention.

---

## What is NexaIQ?

NexaIQ is a **production-grade, multi-tenant B2B SaaS platform** built for companies that want enterprise-grade AI decision intelligence without the enterprise price tag.

At its core, NexaIQ is a **data-to-decision engine**. It takes raw business data and produces:

- **Trained ML models** that predict outcomes such as churn, revenue, and risk
- **Anomaly alerts** written in plain English by an AI — not just numbers in a table
- **Autonomous agent reports** — 4 AI agents investigate anomalies and deliver an executive briefing without any human involvement
- **Natural language answers** to business questions — no SQL knowledge required
- **Document Q&A** — ask questions about your internal reports and get grounded AI answers

The platform is built on a **microservices architecture** with 7 independent services, an event-driven pipeline using **Apache Kafka**, **Apache Airflow** DAG orchestration, **DBT** data transformations, **MLflow** experiment tracking, **ChromaDB** vector store, and **LangGraph** autonomous agents — all monitored by **Prometheus + Grafana**.

---

## How It Works
STEP 1 — INGEST
User uploads CSV via React dashboard
→ Saved to Azure Blob Storage in org-isolated container
→ Kafka fires file.uploaded event
→ Airflow DAG triggered automatically
STEP 2 — TRANSFORM (5-task Airflow DAG)
Task 1: Validate input data
Task 2: DBT transforms RAW → CLEAN → MART
Task 3: AutoML trains XGBoost, LightGBM, RandomForest
MLflow logs all runs and selects best model
Task 4: Anomaly detection runs on all numeric columns
GPT-3.5 writes executive alert in plain English
Task 5: Report dispatched and logged to MongoDB
STEP 3 — DECIDE
Plain English question → SQL → chart in dashboard
PDF upload → ChromaDB embedding → grounded GPT answer
Anomaly → LangGraph agents → executive report in 30 seconds

---

## Architecture

```mermaid
graph TD
    A[React Dashboard] --> B[Auth :8001]
    A --> C[Ingestion :8002]
    A --> D[ML :8003]
    A --> E[Alerts :8004]
    A --> F[Query :8005]
    A --> G[RAG :8007]
    A --> MON[Monitoring :8006]

    C --> KAFKA[Apache Kafka]
    KAFKA --> AIRFLOW[Apache Airflow]
    AIRFLOW --> DBT[DBT RAW to CLEAN to MART]
    AIRFLOW --> D
    AIRFLOW --> E

    D --> MLFLOW[MLflow]
    E --> AGENTS[LangGraph Agents]
    G --> CHROMA[ChromaDB]

    B --> PG[(PostgreSQL)]
    C --> BLOB[(Azure Blob)]
    AGENTS --> MONGO[(MongoDB Atlas)]
```
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
| **Monitoring** | Prometheus · Grafana |

---

## Services

| Service | Port | Description |
|---|---|---|
| Auth | 8001 | JWT auth · Multi-tenant RBAC · Org-scoped isolation |
| Ingestion | 8002 | CSV upload · Azure Blob · Org containers · Pipeline trigger |
| ML | 8003 | AutoML 4 models · MLflow tracking · Model registry |
| Alerts | 8004 | Z-score and IQR detection · GPT executive alerts |
| Query | 8005 | Natural language to SQL · Structured results |
| Monitoring | 8006 | Prometheus metrics · Service health · Response times |
| RAG | 8007 | ChromaDB vector store · Document Q&A · Source attribution |
| MLflow UI | 5000 | Experiment tracking · Model comparison |

---

## Feature Deep Dive

### Multi-Tenant SaaS Architecture
Every organisation gets completely isolated data scoped by org_id at the database level. One company can never access another company's data. Role-based access control enforces Admin, Analyst, and Viewer permissions using JWT tokens with embedded claims.

### Event-Driven Data Pipeline
When a user uploads a CSV, the ingestion service saves it to Azure Blob Storage in an org-specific container, then fires a Kafka event. A consumer reads that event and triggers the Airflow DAG automatically — no polling, no cron jobs, no manual steps.

### Apache Airflow DAG Orchestration
The pipeline is a 5-task DAG with explicit dependency management. Tasks 3 and 4 both depend on Task 2. The scheduler runs on a configurable interval and connects to all live services using authenticated API calls.

### DBT Data Models
Raw data transforms through two DBT models — a staging model that cleans and validates, and a mart model that aggregates business metrics. Both have automated not_null tests and auto-generated lineage documentation.

### AutoML Engine with MLflow
Trains XGBoost, LightGBM, RandomForest, and LogisticRegression simultaneously. Automatically detects classification versus regression. Every run logged to MLflow with parameters, metrics, and artifacts. Best model selected by AUC-ROC or R².

### Anomaly Detection and GenAI Alerts
Z-score and IQR anomaly detection run on every dataset. Anomalies are passed to GPT-3.5 which writes a plain English executive alert referencing specific column names, values, and z-scores.

### Text-to-SQL Interface
Plain English question → GPT generates org-scoped SQL → safety validation blocks dangerous statements → results returned as structured JSON and rendered as charts.

### RAG Pipeline with ChromaDB
Documents split into 500-word overlapping chunks, embedded into ChromaDB with cosine similarity. Top 3 relevant chunks retrieved per question. GPT answers only from provided context with source attribution and relevance scores.

### LangGraph Autonomous Agents
Four agents share typed state: Analyst (root cause) → Report Writer (executive summary) → Critic (quality score 8/10) → Action (alerts, MongoDB log, notifications). Full workflow under 30 seconds.

### Prometheus Monitoring
Tracks request counts, error counts, ML training durations, anomaly counts, upload counts, and service uptime across all 7 services. Health endpoint returns structured JSON with response times for every service.

---

## Project Structure
nexaiq/
├── backend/
│   ├── auth_service/          # JWT + RBAC (port 8001)
│   ├── ingestion_service/     # Azure Blob + DBT pipeline (port 8002)
│   ├── ml_service/            # AutoML + MLflow (port 8003)
│   ├── alert_service/         # Anomaly + GenAI alerts (port 8004)
│   └── query_service/         # Text-to-SQL (port 8005)
├── airflow_dags/              # DAG + Task classes + scheduler
├── agents/                    # LangGraph 4-agent workflow
├── docker/                    # Dockerfiles for all services
├── frontend/                  # React + TypeScript dashboard
├── k8s/                       # Kubernetes deployments + HPA
├── kafka/                     # Producer + consumer + topics
├── mongodb/                   # Atlas client + log service
├── monitoring/                # Prometheus metrics (port 8006)
├── nexaiq_dbt/                # DBT staging + mart models
├── rag/                       # ChromaDB + RAG pipeline (port 8007)
├── docker-compose.yml
├── start.sh
└── .env.example

---

## Quick Start

```bash
git clone https://github.com/Momna-bit/Nexaiq.git
cd Nexaiq
cp .env.example .env

pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose bcrypt \
  azure-storage-blob openai scikit-learn xgboost lightgbm mlflow pandas \
  pymongo chromadb langchain langgraph prometheus-client dbt-core \
  dbt-postgres kafka-python scipy python-dotenv

psql -U postgres -c "CREATE DATABASE nexaiq_db;"

bash start.sh

cd frontend && npm install && npm run dev
```

Open `http://localhost:5173` and register your organisation.

---

## API Reference

### Auth (8001)
POST /auth/register   Register organisation and admin user
POST /auth/login      Authenticate and get JWT token
GET  /auth/me         Get current user profile

### ML (8003)
POST /train           Run AutoML on dataset
GET  /models          List trained models with accuracy scores

### Alerts (8004)
POST /detect-anomalies    Detect anomalies and generate AI alert
POST /ml-insight          Generate business summary of ML results

### Query (8005)
POST /ask             Natural language to SQL to results
GET  /schema          List available tables

### Monitoring (8006)
GET  /health          Service health and response times
GET  /metrics         Prometheus metrics

### RAG (8007)
POST /ingest          Add document to ChromaDB
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

2 replicas per service · HPA scales to 5 at 70% CPU · Liveness probes included

### Azure
```bash
az containerapp up --name nexaiq \
  --resource-group nexaiq-rg \
  --image nexaiq/auth-service:latest \
  --target-port 8001
```

---

## Technical Decisions

**Microservices** — each service scales and deploys independently without affecting others.

**Kafka over direct API calls** — decouples upload from pipeline. Events are durable and replayable.

**DBT over raw SQL** — versioned, tested, documented transformations with lineage graphs.

**LangGraph** — multi-agent workflows produce measurably higher quality outputs than single prompts.

**ChromaDB cosine similarity** — outperforms Euclidean distance for semantic search on normalised embeddings.

**Polyglot persistence** — PostgreSQL for ACID-compliant operational data, MongoDB for flexible event logs.

---

## Skills Demonstrated

| Area | Skills |
|---|---|
| **Data Engineering** | Airflow · DBT · Kafka · Azure Blob · ETL · RAW→CLEAN→MART |
| **ML Engineering** | AutoML · XGBoost · LightGBM · MLflow · Evidently AI · anomaly detection |
| **AI Engineering** | OpenAI API · LangGraph · ChromaDB · RAG · prompt engineering · agents |
| **Backend** | FastAPI · PostgreSQL · MongoDB · SQLAlchemy · JWT · RBAC · microservices |
| **Frontend** | React · TypeScript · Tailwind · Recharts · Zustand |
| **DevOps** | Docker · Kubernetes · GitHub Actions · Prometheus · Grafana |
| **Cloud** | Azure Blob Storage · Azure Container Apps · MongoDB Atlas |

---

## Built By

**Momna Ali** — Data Engineer and ML Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/momna-ali)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-6d28d9?style=flat-square)](https://momna-bit.github.io)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/Momna-bit)

---

## License

MIT — see LICENSE for details.
