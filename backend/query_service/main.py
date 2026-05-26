from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from jose import jwt
from sql_generator import generate_sql, validate_sql
import os
from dotenv import load_dotenv

load_dotenv("../../.env")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "nexaiq-super-secret-key-2025")
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL)

app = FastAPI(title="NexaIQ Query Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8001/auth/login"
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(401, "Invalid token")

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "NexaIQ Query Service running"}

@app.post("/ask")
def ask(
    request: QueryRequest,
    user=Depends(get_current_user)
):
    try:
        org_id = user["org_id"]

        # Generate SQL from question
        print(f"Question: {request.question}")
        sql = generate_sql(request.question, org_id)
        print(f"Generated SQL: {sql}")

        # Validate SQL is safe
        if not validate_sql(sql):
            raise HTTPException(400, "Unsafe SQL generated")

        # Run query
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = list(result.keys())

        # Format results
        data = [dict(zip(columns, row)) for row in rows]

        return {
            "question": request.question,
            "sql": sql,
            "columns": columns,
            "data": data,
            "row_count": len(data)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/schema")
def get_schema(user=Depends(get_current_user)):
    """Return available tables for the user"""
    org_id = user["org_id"]
    try:
        with engine.connect() as conn:
            # Get datasets for this org
            result = conn.execute(
                text("SELECT filename, status, row_count, created_at FROM datasets WHERE org_id = :org_id"),
                {"org_id": org_id}
            )
            datasets = [dict(zip(result.keys(), row)) for row in result.fetchall()]

        return {
            "org_id": org_id,
            "datasets": datasets,
            "available_tables": [
                "clean_data",
                "raw_data",
                "mart_summary",
                "ml_models",
                "datasets"
            ]
        }
    except Exception as e:
        raise HTTPException(500, str(e))
