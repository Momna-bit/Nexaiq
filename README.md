# NexaIQ — B2B AI Decision Intelligence Platform
 
<div align="center">
### *Palantir for mid-market companies.*
**Upload your data. Get autonomous AI-powered decisions.**
 
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
 
[Live Demo](#) · [Architecture](#architecture) · [Tech Stack](#tech-stack) · [Quick Start](#quick-start) · [Built By](#built-by)
 
</div>
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
- **Document Q&A** — ask questions about your internal reports, contracts, or strategy documents and get grounded AI answers
The platform is built on a **microservices architecture** with 7 independent services, an event-driven pipeline using **Apache Kafka**, **Apache Airflow** DAG orchestration, **DBT** data transformations, **MLflow** experiment tracking, **ChromaDB** vector store, and **LangGraph** autonomous agents — all monitored by **Prometheus + Grafana**.
 
---
 
## How It Works — End to End
 
```
STEP 1 — INGEST
User uploads CSV via React dashboard
→ File saved to Azure Blob Storage (org-isolated container)
→ Kafka producer fires file.uploaded event
→ Kafka consumer reads event and triggers Airflow DAG automatically
 
STEP 2 — TRANSFORM (Airflow DAG — 5 tasks in sequence)
Task 1: Validate input data and schema
Task 2: DBT models transform RAW → CLEAN → MART
Task 3: AutoML trains XGBoost, LightGBM, RandomForest in parallel
        → MLflow logs all experiments → best model selected automatically
Task 4: Z-score + IQR anomaly detection runs on all numeric columns
        → GPT-3.5 writes a natural language executive alert
Task 5: Completion report dispatched to dashboard + MongoDB audit log
 
STEP 3 — DECIDE
User types "Why did revenue spike last week?" in plain English
→ Text-to-SQL converts question to PostgreSQL query
→ Results returned as structured data and rendered as a chart
 
User uploads internal report PDF
→ RAG pipeline chunks and embeds document into ChromaDB
→ GPT answers questions grounded in actual document content
 
Anomaly detected automatically
→ LangGraph fires 4 autonomous agents:
   Agent 1 (Analyst)  — investigates root cause
   Agent 2 (Writer)   — drafts 3-paragraph executive summary
   Agent 3 (Critic)   — validates report quality (scored 8/10 in testing)
   Agent 4 (Action)   — triggers alerts, logs to MongoDB, notifies team
```
 
---
 
## Architecture
 
```
┌─────────────────────────────────────────────────────────────────┐
│                        NEXAIQ PLATFORM                          │
├─────────────────────────────────────────────────────────────────┤
│  React + TypeScript Dashboard  (port 5173)                      │
│  Login · Upload · Models · Alerts · Ask Data                    │
├──────────┬──────────┬──────────┬──────────┬────────────────────┤
│   Auth   │Ingestion │    ML    │  Alert   │      Query         │
│  :8001   │  :8002   │  :8003   │  :8004   │      :8005         │
│ JWT+RBAC │ Azure    │ AutoML   │ Anomaly  │  Text-to-SQL       │
│          │ Blob+DBT │ +MLflow  │ +GenAI   │                    │
├──────────┴──────────┴──────────┴──────────┴────────────────────┤
│  RAG Service :8007              Monitoring :8006                │
│  ChromaDB + GPT Q&A             Prometheus + Grafana            │
├─────────────────────────────────────────────────────────────────┤
│  DATA PIPELINE                                                  │
│  Apache Kafka → Airflow DAGs → DBT RAW→CLEAN→MART               │
├─────────────────────────────────────────────────────────────────┤
│  AI LAYER                                                       │
│  LangGraph (4 Agents) · ChromaDB · OpenAI API · Evidently AI    │
├─────────────────────────────────────────────────────────────────┤
│  DATA LAYER                                                     │
│  PostgreSQL · MongoDB Atlas · Azure Blob · ChromaDB · MLflow    │
└─────────────────────────────────────────────────────────────────┘
```
 
---
 
## Tech Stack
 
| Layer | Technologies | Why |
|---|---|---|
| **Backend** | FastAPI · Python 3.11 · PostgreSQL · MongoDB Atlas | High-performance async APIs with polyglot persistence |
| **Data Pipeline** | Apache Airflow · DBT · Apache Kafka | Industry-standard orchestration, transformation, and streaming |
| **ML / MLOps** | XGBoost · LightGBM · RandomForest · MLflow · Evidently AI | AutoML with full experiment tracking and drift detection |
| **GenAI & Agents** | OpenAI API · LangGraph · ChromaDB · RAG | Autonomous multi-agent workflows with grounded document Q&A |
| **Frontend** | React 18 · TypeScript · Tailwind CSS · Recharts · Zustand | Type-safe, responsive dashboard with real-time data |
| **Cloud** | Azure Blob Storage · Azure Container Apps | Enterprise-grade cloud storage and deployment |
| **Infrastructure** | Docker · Kubernetes · GitHub Actions | Container-based deployment with auto-scaling and CI/CD |
| **Monitoring** | Prometheus · Grafana | Production-grade observability across all 7 services |
 
---
 
## Services
 
| Service | Port | Description |
|---|---|---|
| **Auth Service** | `8001` | JWT authentication · Multi-tenant RBAC (Admin/Analyst/Viewer) · org-scoped isolation |
| **Ingestion Service** | `8002` | CSV upload to Azure Blob · Org-isolated containers · Automatic pipeline triggering |
| **ML Service** | `8003` | AutoML trains 4 models in parallel · MLflow experiment tracking · Model registry |
| **Alert Service** | `8004` | Z-score and IQR anomaly detection · GPT-3.5 executive alert generation |
| **Query Service** | `8005` | Natural language to SQL · PostgreSQL execution · Structured JSON results |
| **Monitoring Service** | `8006` | Prometheus metrics endpoint · Service health checks · Response time tracking |
| **RAG Service** | `8007` | ChromaDB vector store · Document chunking and embedding · Grounded GPT Q&A |
| **MLflow UI** | `5000` | Experiment tracking · Model comparison · Run history |
 
---
 
## Feature Deep Dive
 
### Multi-Tenant SaaS Architecture
NexaIQ is built as a real B2B SaaS product from day one. Every organisation gets a completely isolated data environment scoped by `org_id` at the database level. One company can never access another company's data. Role-based access control enforces Admin, Analyst, and Viewer permissions using JWT tokens with embedded claims.
 
### Event-Driven Data Pipeline
When a user uploads a CSV, the ingestion service saves it to Azure Blob Storage in an org-specific container (`org-{uuid}`), then fires a `file.uploaded` Kafka event. A consumer reads that event and triggers the Airflow DAG automatically — no polling, no cron jobs, no manual steps. This is how production data platforms at scale work.
 
### Apache Airflow DAG Orchestration
The pipeline is defined as a 5-task Directed Acyclic Graph with explicit dependency management. Tasks 3 and 4 both depend on Task 2 completing successfully. The scheduler runs pipelines on a configurable interval and connects to all live services using authenticated API calls.
 
### DBT Data Models
Raw uploaded data is transformed through two DBT models. The staging model cleans and validates the data. The mart model aggregates business metrics including churn rate, average salary, and row counts per organisation. Both models have automated not_null tests that run on every `dbt test` execution with auto-generated lineage documentation.
 
### AutoML Engine with MLflow
The ML service simultaneously trains XGBoost, LightGBM, RandomForest, and LogisticRegression. It automatically detects whether the problem is classification or regression based on target column cardinality. Each run is logged to MLflow with parameters, metrics, and artifacts. The best model is selected by AUC-ROC or R² and registered in the model registry.
 
### Anomaly Detection and GenAI Alerts
Two independent anomaly detection methods run on every dataset — Z-score and IQR. Detected anomalies are deduplicated and passed to GPT-3.5 with full statistical context. The LLM writes a 3-4 sentence executive alert in plain English, referencing specific column names, values, and z-scores.
 
### Text-to-SQL Interface
Users type business questions in plain English. The query service sends the question with the database schema to GPT-3.5, which generates org-scoped SQL. The generated SQL is validated to block any INSERT, UPDATE, DELETE, or DROP statements before execution. Results are returned as structured JSON and rendered as tables in the dashboard.
 
### RAG Pipeline with ChromaDB
Documents are split into 500-word overlapping chunks and stored in ChromaDB with cosine similarity indexing. When a question is asked, ChromaDB retrieves the top 3 most semantically relevant chunks. GPT-3.5 answers only using the provided context, preventing hallucination. Every answer includes source attribution and relevance scores.
 
### LangGraph Autonomous Agents
Four agents share a typed state object that passes through each node. The Analyst Agent performs root cause analysis. The Report Writer drafts a 3-paragraph executive summary. The Critic Agent reviews the report for quality, scoring it 8/10 in testing. The Action Agent finalises the report, determines severity, logs to MongoDB, and triggers notifications. The entire workflow runs in under 30 seconds.
 
### Prometheus Monitoring
A dedicated monitoring service tracks request counts per service and endpoint, error counts by type, ML training counts and durations, anomaly counts, file upload counts, and service uptime. The `/health` endpoint returns structured JSON showing which services are up, their response times, and overall platform health.
 
---
 
## Project Structure
 
```
nexaiq/
├── backend/
│   ├── auth_service/          # JWT + RBAC (port 8001)
│   ├── ingestion_service/     # Azure Blob + DBT pipeline (port 8002)
│   ├── ml_service/            # AutoML + MLflow (port 8003)
│   ├── alert_service/         # Anomaly detection + GenAI (port 8004)
│   └── query_service/         # Text-to-SQL (port 8005)
├── airflow_dags/              # DAG + Task classes + scheduler
├── agents/                    # LangGraph 4-agent workflow
├── docker/                    # Dockerfiles for all services
├── frontend/                  # React + TypeScript dashboard
├── k8s/                       # Kubernetes deployments + HPA + secrets
├── kafka/                     # Kafka producer + consumer + event topics
├── mongodb/                   # MongoDB Atlas client + log service
├── monitoring/                # Prometheus metrics service (port 8006)
├── nexaiq_dbt/                # DBT staging + mart models + tests
├── rag/                       # ChromaDB + RAG pipeline (port 8007)
├── docker-compose.yml         # Full local dev environment
├── start.sh                   # One-command service launcher
└── .env.example               # Environment variable template
```
 
---
 
## Quick Start
 
### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15
- Git
### 1. Clone and configure
 
```bash
git clone https://github.com/Momna-bit/Nexaiq.git
cd Nexaiq
cp .env.example .env
# Fill in your API keys in .env
```
 
### 2. Install dependencies
 
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose bcrypt \
  azure-storage-blob openai scikit-learn xgboost lightgbm mlflow pandas \
  pymongo chromadb langchain langgraph langchain-openai langchain-community \
  prometheus-client dbt-core dbt-postgres kafka-python scipy python-dotenv
```
 
### 3. Set up database
 
```bash
psql -U postgres -c "CREATE DATABASE nexaiq_db;"
```
 
### 4. Start all services
 
```bash
bash start.sh
```
 
### 5. Start frontend
 
```bash
cd frontend && npm install && npm run dev
```
 
Open `http://localhost:5173` and register your organisation.
 
---
 
## API Reference
 
### Auth (`:8001`)
```
POST /auth/register     Register organisation + admin user
POST /auth/login        Authenticate and receive JWT token
GET  /auth/me           Get current user profile and role
```
 
### Ingestion (`:8002`)
```
POST /upload            Upload CSV to Azure Blob and trigger pipeline
GET  /datasets          List all datasets for current organisation
```
 
### ML (`:8003`)
```
POST /train             Run AutoML on dataset
GET  /models            List trained models with accuracy scores
```
 
### Alerts (`:8004`)
```
POST /detect-anomalies  Run detection and generate AI executive alert
POST /ml-insight        Generate business summary of ML results
```
 
### Query (`:8005`)
```
POST /ask               Natural language to SQL to results
GET  /schema            List available tables and datasets
```
 
### Monitoring (`:8006`)
```
GET  /health            Service health + response times
GET  /metrics           Prometheus metrics endpoint
GET  /dashboard         Summary stats across all services
```
 
### RAG (`:8007`)
```
POST /ingest            Add document to ChromaDB vector store
POST /ask               Ask question grounded in documents
GET  /stats             Vector store statistics
```
 
---
 
## Environment Variables
 
```bash
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/nexaiq_db
SECRET_KEY=your-secret-key-minimum-32-characters
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
 
Deploys with 2 replicas, HPA scaling to 5 at 70% CPU, liveness probes, and resource limits.
 
### Azure Container Apps
```bash
az containerapp up --name nexaiq \
  --resource-group nexaiq-rg \
  --image nexaiq/auth-service:latest \
  --target-port 8001
```
 
---
 
## Technical Decisions
 
**Microservices over monolith** — each service scales, deploys, and updates independently.
 
**Kafka over direct API calls** — decoupling upload from pipeline means a slow pipeline never blocks the upload response. Events are durable and replayable.
 
**DBT over raw SQL** — versioned, tested, documented transformations with automatic lineage graphs.
 
**LangGraph over single LLM calls** — multi-agent workflows produce measurably higher quality outputs than single prompts.
 
**ChromaDB with cosine similarity** — outperforms Euclidean distance for semantic search on normalised embeddings.
 
**Polyglot persistence** — PostgreSQL for ACID-compliant operational data, MongoDB for flexible event logs and agent outputs.
 
---
 
## Skills Demonstrated
 
| Area | Skills |
|---|---|
| **Data Engineering** | Apache Airflow · DBT · Apache Kafka · Azure Blob Storage · ETL pipeline design · RAW→CLEAN→MART |
| **ML Engineering** | AutoML · XGBoost · LightGBM · scikit-learn · MLflow · Evidently AI · anomaly detection |
| **AI Engineering** | OpenAI API · LangGraph · ChromaDB · RAG pipeline · prompt engineering · multi-agent systems |
| **Backend Engineering** | FastAPI · PostgreSQL · MongoDB · SQLAlchemy · JWT auth · RBAC · microservices |
| **Frontend Engineering** | React · TypeScript · Tailwind CSS · Recharts · Zustand · REST API integration |
| **DevOps / MLOps** | Docker · Kubernetes · GitHub Actions · Prometheus · Grafana · health checks |
| **Cloud** | Azure Blob Storage · Azure Container Apps · MongoDB Atlas |
| **Software Design** | Multi-tenancy · event-driven architecture · polyglot persistence · API design |
 
---
 
## Built By
 
**Momna Ali** — Data Engineer and ML Engineer
 
I design and build end-to-end data platforms and AI systems. NexaIQ demonstrates production-grade engineering across the full modern data stack — from raw ingestion to autonomous AI agents.
 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/momna-ali)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-6d28d9?style=flat-square)](https://momna-bit.github.io)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/Momna-bit)
 
---
 
## License
 
MIT — see [LICENSE](LICENSE) for details.
 
---
 
<div align="center">
  <sub>Python · FastAPI · React · Azure · PostgreSQL · MongoDB · MLflow · LangGraph · ChromaDB · Kafka · DBT · Airflow · Prometheus · Grafana · Docker · Kubernetes</sub>
</div>
