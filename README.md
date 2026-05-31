<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=220&section=header&text=NexaIQ&fontSize=80&fontColor=C6FF00&animation=twinkling&fontAlignY=40&desc=Autonomous%20Data%20Intelligence%20Platform&descAlignY=62&descSize=22&descColor=ffffff" width="100%"/>

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=18&pause=1000&color=C6FF00&center=true&vCenter=true&width=700&lines=Upload+a+CSV.+Get+AI+decisions+in+under+5+minutes.;7+Microservices+%C2%B7+4+AI+Agents+%C2%B7+Production+B2B+SaaS;Palantir+for+Mid-Market+Companies;Zero+Data+Team+Required." alt="Typing SVG"/>

<br/>

[![Portfolio](https://img.shields.io/badge/📊%20Case%20Study-Portfolio-C6FF00?style=for-the-badge&logoColor=black)](https://momna-bit.github.io/nexaiq-portfolio)
[![Dashboard](https://img.shields.io/badge/🖥️%20Live%20Dashboard-Open%20App-00CFFF?style=for-the-badge)](https://momna-bit.github.io/Nexaiq)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Momna%20Ali-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/momna-ali)

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white)
![DBT](https://img.shields.io/badge/DBT-FF694B?style=flat-square&logo=dbt&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)

</div>

---

## 🎯 What is NexaIQ?

> **"Palantir for mid-market companies."**
>
> NexaIQ is a production-grade B2B SaaS platform that turns raw business data into autonomous AI decisions — no data team required. Upload a CSV. The platform handles everything else automatically in under 5 minutes.

Mid-market companies (50–500 employees) have real business data but no affordable way to act on it. A full data team costs $500K+/year. Tools like Palantir cost millions. Power BI shows charts but doesn't think for you. **NexaIQ fixes that.**

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| 🏆 **Portfolio & Case Study** | [momna-bit.github.io/nexaiq-portfolio](https://momna-bit.github.io/nexaiq-portfolio) |
| 🖥️ **Live Dashboard** | [momna-bit.github.io/Nexaiq](https://momna-bit.github.io/Nexaiq) |
| 📊 **MLflow Tracking** | `http://localhost:5000` (run locally) |
| 💼 **LinkedIn** | [linkedin.com/in/momna-ali](https://www.linkedin.com/in/momna-ali) |
| 📧 **Contact** | [alimomna87@gmail.com](mailto:alimomna87@gmail.com) |

---

## ⚡ Pipeline Overview

```
CSV Upload → Azure Blob → Kafka Event → Airflow DAG → DBT Transform
    → AutoML Training → Anomaly Detection → GPT Alert → LangGraph Agents
                    ⏱️ Under 5 minutes. Zero human intervention.
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│               React Dashboard (GitHub Pages)                  │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                  7 FastAPI Microservices                       │
│  Auth:8001  │  Ingestion:8002  │  ML:8003  │  Alerts:8004    │
│  Query:8005 │  Monitoring:8006 │  RAG:8007                   │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│   Apache Kafka (4 topics) ──────► Apache Airflow DAGs         │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│  PostgreSQL │ MongoDB Atlas │ Azure Blob │ ChromaDB │ MLflow  │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│  OpenAI GPT-3.5 │ LangGraph 4 Agents │ RAG Pipeline          │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 How It Works

### 01 — Secure Ingestion
```python
POST /ingest/upload
# CSV → Azure Blob (org-isolated container)
# Kafka fires: file.uploaded
# Airflow DAG triggers automatically
# DBT: RAW → CLEAN → MART
```

### 02 — AutoML Training
```python
# 4 models train simultaneously
XGBoost · LightGBM · RandomForest · LogisticRegression
# Best model auto-selected by AUC score
# All 61+ runs logged → http://localhost:5000
```

### 03 — Anomaly Detection
```python
# Z-Score + IQR on every column
# Detects: revenue spikes, churn shifts, inventory drops
# Instant — fires the moment data lands
```

### 04 — GPT Executive Alert
```
"Revenue in Q4 is 2.65 standard deviations above the mean,
suggesting an unusual revenue spike. Investigation recommended."
— Written by GPT-3.5, no analyst needed
```

### 05 — Text-to-SQL
```
User:   "Why did revenue drop last month?"
GPT:    SELECT region, SUM(revenue) FROM mart_sales WHERE...
Result: Structured table — zero SQL knowledge needed
```

### 06 — Autonomous Agents
```
Analyst Agent    → finds root cause
Report Writer    → drafts executive summary
Critic Agent     → validates (threshold: 8/10)
Action Agent     → fires alerts
Total: < 30 seconds. Zero human intervention.
```

---

## 📊 MLflow Experiment Tracking

```bash
# Starts automatically with platform
# Access at: http://localhost:5000
```

**61+ experiment runs** tracked across XGBoost, LightGBM, RandomForest, LogisticRegression

**Compare models:**
1. Open `http://localhost:5000`
2. Select experiment → click multiple runs → **Compare**
3. View side-by-side accuracy, AUC, F1 score charts
4. Best model auto-registered in Model Registry

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Languages** | Python 3.11, TypeScript |
| **Backend** | FastAPI, SQLAlchemy, Pydantic |
| **Frontend** | React 18, TypeScript, Tailwind CSS, Recharts, Zustand |
| **Data Pipeline** | Apache Airflow, Apache Kafka (4 topics), DBT |
| **ML / MLOps** | XGBoost, LightGBM, RandomForest, MLflow, Evidently AI |
| **AI / GenAI** | OpenAI GPT-3.5, LangGraph, ChromaDB, RAG Pipeline |
| **Databases** | PostgreSQL, MongoDB Atlas, ChromaDB |
| **Cloud** | Azure Blob Storage, Azure Container Apps |
| **Infra** | Docker, Kubernetes HPA (5 replicas), GitHub Actions |
| **Monitoring** | Prometheus, Grafana, Liveness/Readiness Probes |

---

## 🗂️ Project Structure

```
nexaiq/
├── backend/
│   ├── auth_service/        # Port 8001 — JWT + RBAC + Multi-tenant
│   ├── ingestion_service/   # Port 8002 — Azure Blob + DBT pipeline
│   ├── ml_service/          # Port 8003 — AutoML + MLflow tracking
│   ├── alert_service/       # Port 8004 — Anomaly detection + GPT alerts
│   └── query_service/       # Port 8005 — Text-to-SQL
├── airflow_dags/            # 5-task DAG pipeline
├── agents/                  # LangGraph 4-agent workflow
├── docker/                  # Dockerfiles for all services
├── frontend/                # React 18 + TypeScript dashboard
├── k8s/                     # Kubernetes + HPA configs
├── kafka/                   # Kafka producer + consumer
├── mongodb/                 # MongoDB Atlas client
├── monitoring/              # Port 8006 — Prometheus
├── nexaiq_dbt/              # DBT models + tests (PASS=2, WARN=0)
├── rag/                     # Port 8007 — ChromaDB + RAG
├── start.sh                 # Start all services
├── docker-compose.yml       # Local dev environment
└── .env.example             # Environment template
```

---

## ⚙️ Local Setup

```bash
# 1. Clone
git clone https://github.com/Momna-bit/Nexaiq.git
cd Nexaiq

# 2. Environment
cp .env.example .env
# Add your API keys to .env

# 3. Kill existing ports (if needed)
for port in 8001 8002 8003 8004 8005 8006 8007 5000; do
  pid=$(netstat -ano | grep ":$port " | grep LISTENING | awk '{print $5}' | head -1)
  if [ ! -z "$pid" ]; then taskkill //F //PID $pid 2>/dev/null; fi
done

# 4. Start all services
bash start.sh

# 5. Start monitoring (manual)
cd monitoring && uvicorn main:app --port 8006 &

# 6. Start frontend
cd frontend && npm install && npm run dev
```

**Service URLs:**
```
Auth         → http://127.0.0.1:8001
Ingestion    → http://127.0.0.1:8002
ML           → http://127.0.0.1:8003
Alerts       → http://127.0.0.1:8004
Query        → http://127.0.0.1:8005
Monitoring   → http://127.0.0.1:8006
RAG          → http://127.0.0.1:8007
MLflow UI    → http://127.0.0.1:5000
Frontend     → http://localhost:5173
```

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## ☸️ Kubernetes

```bash
kubectl apply -f k8s/
kubectl get pods
kubectl get hpa   # scales to 5 replicas at 70% CPU
```

---

## 📡 API Reference

```
Auth :8001     POST /auth/login · GET /auth/me
Ingest :8002   POST /ingest/upload · GET /ingest/status/{id}
ML :8003       POST /ml/train · GET /ml/models · GET /ml/runs
Alerts :8004   GET /alerts · POST /alerts/detect
Query :8005    POST /query/ask · GET /query/history
RAG :8007      POST /rag/upload · POST /rag/ask
```

---

## 📋 What This Demonstrates

| Domain | Skills |
|--------|--------|
| **Data Engineering** | Airflow, DBT, Kafka, Azure Blob, ETL, multi-layer warehouse |
| **ML Engineering** | AutoML, MLflow, model registry, experiment tracking |
| **AI Engineering** | RAG pipeline, LangGraph agents, vector search, prompt engineering |
| **Backend Engineering** | 7 microservices, FastAPI, PostgreSQL, MongoDB, JWT, RBAC |
| **Frontend Engineering** | React 18, TypeScript, enterprise UI design |
| **DevOps** | Docker, Kubernetes, GitHub Actions, Prometheus, Grafana |
| **Cloud** | Azure Blob Storage, Azure Container Apps, MongoDB Atlas |

---

## 🔐 Security

- JWT authentication + RBAC (Admin / Analyst / Viewer)
- Multi-tenant org isolation — every user scoped by `org_id`
- Azure Blob org-isolated containers
- All secrets via `os.getenv()` — never hardcoded
- `.env` in `.gitignore`

---

## 👩‍💻 Built By

**Momna Ali** — Data Engineer · ML Engineer · AI Engineer · Data Scientist

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/momna-ali)
[![Portfolio](https://img.shields.io/badge/Portfolio-NexaIQ-C6FF00?style=for-the-badge)](https://momna-bit.github.io/nexaiq-portfolio)
[![Dashboard](https://img.shields.io/badge/Dashboard-Live-00CFFF?style=for-the-badge)](https://momna-bit.github.io/Nexaiq)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:alimomna87@gmail.com)

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer&animation=twinkling" width="100%"/>

*⭐ Star this repo if you find it impressive!*
</div>
