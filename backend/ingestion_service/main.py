from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from blob_storage import upload_file
from jose import jwt
import os, uuid, datetime
from dotenv import load_dotenv

load_dotenv("../../.env")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "nexaiq-super-secret-key-2025")
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(String, nullable=False)
    blob_url = Column(String, nullable=False)
    status = Column(String, default="uploaded")
    row_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexaIQ Ingestion Service")
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

@app.get("/")
def root():
    return {"message": "NexaIQ Ingestion Service running"}

@app.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Only CSV files allowed")

    file_bytes = await file.read()
    org_id = user["org_id"]
    filename = f"{uuid.uuid4()}_{file.filename}"

    try:
        blob_url = upload_file(file_bytes, org_id, filename)
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {str(e)}")

    dataset = Dataset(
        org_id=org_id,
        filename=file.filename,
        blob_url=blob_url,
        status="uploaded"
    )
    db.add(dataset)
    db.commit()

    try:
        from pipeline import run_pipeline
        mart = run_pipeline(
            org_id=org_id,
            dataset_id=str(dataset.id),
            blob_filename=filename
        )
        dataset.status = "processed"
        dataset.row_count = mart["total_rows"]
        db.commit()
    except Exception as e:
        print(f"Pipeline error: {e}")

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "blob_url": blob_url,
        "dataset_id": str(dataset.id)
    }

@app.get("/datasets")
def get_datasets(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    org_id = user["org_id"]
    datasets = db.query(Dataset).filter(
        Dataset.org_id == org_id
    ).all()
    return [{
        "id": str(d.id),
        "filename": d.filename,
        "status": d.status,
        "created_at": str(d.created_at)
    } for d in datasets]
