import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, mean_squared_error, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
import os
from dotenv import load_dotenv

load_dotenv("../../.env")
mlflow.set_tracking_uri("http://127.0.0.1:5000")

def detect_problem_type(df, target_col):
    if df[target_col].nunique() <= 10:
        return "classification"
    return "regression"

def prepare_data(df, target_col):
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        if col != target_col:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return train_test_split(X, y, test_size=0.2, random_state=42)

def get_models(problem_type):
    if problem_type == "classification":
        return {
            "LogisticRegression": LogisticRegression(max_iter=1000),
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
            "XGBoost": XGBClassifier(random_state=42, eval_metric="logloss"),
            "LightGBM": LGBMClassifier(random_state=42, verbose=-1),
        }
    return {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost": XGBRegressor(random_state=42),
        "LightGBM": LGBMRegressor(random_state=42, verbose=-1),
    }

def evaluate_model(model, X_test, y_test, problem_type):
    y_pred = model.predict(X_test)
    if problem_type == "classification":
        metrics = {
            "accuracy": round(accuracy_score(y_test, y_pred), 4),
            "f1_score": round(f1_score(y_test, y_pred, average="weighted"), 4),
        }
        try:
            if len(set(y_test)) > 1:
                y_prob = model.predict_proba(X_test)[:, 1]
                metrics["auc_roc"] = round(roc_auc_score(y_test, y_prob), 4)
        except Exception:
            pass
    else:
        metrics = {
            "r2_score": round(r2_score(y_test, y_pred), 4),
            "rmse": round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        }
    return metrics

def run_automl(df, target_col, dataset_id, org_id):
    print(f"🤖 Starting AutoML for dataset {dataset_id}")
    problem_type = detect_problem_type(df, target_col)
    print(f"📊 Problem type: {problem_type}")
    X_train, X_test, y_train, y_test = prepare_data(df, target_col)
    print(f"📦 Training: {len(X_train)} rows, Test: {len(X_test)} rows")
    models = get_models(problem_type)
    results = []
    best_model = None
    best_score = -999
    best_model_name = ""
    mlflow.set_experiment(f"nexaiq-{org_id[:8]}")
    for model_name, model in models.items():
        print(f"⚡ Training {model_name}...")
        with mlflow.start_run(run_name=f"{model_name}-{dataset_id[:8]}"):
            model.fit(X_train, y_train)
            metrics = evaluate_model(model, X_test, y_test, problem_type)
            mlflow.log_param("model_name", model_name)
            mlflow.log_param("problem_type", problem_type)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, artifact_path=model_name)
            score = metrics.get("auc_roc", metrics.get("accuracy", metrics.get("r2_score", 0)))
            results.append({
                "model_name": model_name,
                "metrics": metrics,
                "score": score
            })
            if score > best_score:
                best_score = score
                best_model = model
                best_model_name = model_name
            print(f"✅ {model_name}: {metrics}")
    print(f"\n🏆 Best model: {best_model_name} (score: {best_score})")
    return {
        "problem_type": problem_type,
        "target_column": target_col,
        "best_model": best_model_name,
        "best_score": best_score,
        "all_results": results,
        "dataset_id": dataset_id
    }
