from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from jose import jwt
from rag_pipeline import ingest_document, answer_question
from vector_store import get_collection_stats
import os

SECRET_KEY = "nexaiq-super-secret-key-2025"
ALGORITHM = "HS256"

app = FastAPI(title="NexaIQ RAG Service")
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

class IngestRequest(BaseModel):
    text: str
    doc_name: str
    doc_type: str = "text"

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "NexaIQ RAG Service running"}

@app.post("/ingest")
def ingest(request: IngestRequest, user=Depends(get_current_user)):
    try:
        org_id = user["org_id"]
        result = ingest_document(
            org_id=org_id,
            text=request.text,
            doc_name=request.doc_name,
            doc_type=request.doc_type
        )
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/ask")
def ask(request: QuestionRequest, user=Depends(get_current_user)):
    try:
        org_id = user["org_id"]
        result = answer_question(
            org_id=org_id,
            question=request.question
        )
        return result
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/stats")
def stats(user=Depends(get_current_user)):
    try:
        org_id = user["org_id"]
        return get_collection_stats(org_id)
    except Exception as e:
        raise HTTPException(500, str(e))
