from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from jose import jwt
from automl import run_automl
import pandas as pd
import os, uuid, datetime
from dotenv import load_dotenv

load_dotenv("../../.env")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "nexaiq-super-secret-key-2025")
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MLModel(Base):
    __tablename__ = "ml_models"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    dataset_id = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    problem_type = Column(String, nullable=False)
    best_score = Column(Float, nullable=False)
    target_column = Column(String, nullable=False)
    status = Column(String, default="trained")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexaIQ ML Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(401, "Invalid token")

class TrainRequest(BaseModel):
    dataset_id: str
    target_column: str
    data: list

@app.get("/")
def root():
    return {"message": "NexaIQ ML Service running"}

@app.post("/train")
def train(
    request: TrainRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        df = pd.DataFrame(request.data)
        org_id = user["org_id"]
        result = run_automl(
            df=df,
            target_col=request.target_column,
            dataset_id=request.dataset_id,
            org_id=org_id
        )
        # Save to database
        ml_model = MLModel(
            org_id=org_id,
            dataset_id=request.dataset_id,
            model_name=result["best_model"],
            problem_type=result["problem_type"],
            best_score=result["best_score"],
            target_column=request.target_column
        )
        db.add(ml_model)
        db.commit()
        return {
            "message": "Training complete",
            "best_model": result["best_model"],
            "best_score": result["best_score"],
            "all_results": result["all_results"],
            "model_id": str(ml_model.id)
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/models")
def get_models(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    org_id = user["org_id"]
    models = db.query(MLModel).filter(MLModel.org_id == org_id).all()
    return [{
        "id": str(m.id),
        "model_name": m.model_name,
        "problem_type": m.problem_type,
        "best_score": m.best_score,
        "target_column": m.target_column,
        "status": m.status,
        "created_at": str(m.created_at)
    } for m in models]
