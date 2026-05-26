from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt
from anomaly import run_anomaly_detection
from llm_alert import generate_alert, generate_ml_insight
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv("../../.env")

SECRET_KEY = os.getenv("SECRET_KEY", "nexaiq-super-secret-key-2025")
ALGORITHM = "HS256"

app = FastAPI(title="NexaIQ Alert Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(401, "Invalid token")

class AnomalyRequest(BaseModel):
    data: list
    dataset_name: str = "Business Dataset"

class MLInsightRequest(BaseModel):
    problem_type: str
    best_model: str
    best_score: float
    target_column: str

@app.get("/")
def root():
    return {"message": "NexaIQ Alert Service running"}

@app.post("/detect-anomalies")
def detect_anomalies(
    request: AnomalyRequest,
    user=Depends(get_current_user)
):
    try:
        df = pd.DataFrame(request.data)
        results = run_anomaly_detection(df)

        # Generate LLM alert
        alert_message = generate_alert(
            anomalies=results["anomalies"],
            dataset_info={
                "name": request.dataset_name,
                "rows": results["rows_checked"]
            }
        )

        return {
            "anomalies_found": results["total_anomalies"],
            "anomalies": results["anomalies"],
            "ai_alert": alert_message,
            "columns_checked": results["columns_checked"]
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/ml-insight")
def ml_insight(
    request: MLInsightRequest,
    user=Depends(get_current_user)
):
    try:
        insight = generate_ml_insight(request.dict())
        return {"insight": insight}
    except Exception as e:
        raise HTTPException(500, str(e))
