FROM python:3.11-slim

WORKDIR /app

COPY backend/ml_service/ .

RUN pip install --no-cache-dir \
    fastapi uvicorn sqlalchemy \
    psycopg2-binary python-jose \
    scikit-learn xgboost lightgbm \
    mlflow pandas python-dotenv

EXPOSE 8003

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
