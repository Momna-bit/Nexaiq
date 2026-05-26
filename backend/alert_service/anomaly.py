import pandas as pd
import numpy as np
from scipy import stats

def detect_zscore_anomalies(df: pd.DataFrame, threshold: float = 2.0) -> list:
    """Detect anomalies using Z-score method"""
    anomalies = []
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        col_data = df[col].dropna()
        if len(col_data) < 3:
            continue
        z_scores = np.abs(stats.zscore(col_data))
        anomaly_indices = np.where(z_scores > threshold)[0]
        for idx in anomaly_indices:
            anomalies.append({
                "column": col,
                "index": int(idx),
                "value": float(col_data.iloc[idx]),
                "z_score": round(float(z_scores[idx]), 2),
                "mean": round(float(col_data.mean()), 2),
                "std": round(float(col_data.std()), 2),
                "type": "zscore"
            })

    return anomalies

def detect_iqr_anomalies(df: pd.DataFrame) -> list:
    """Detect anomalies using IQR method"""
    anomalies = []
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        col_data = df[col].dropna()
        if len(col_data) < 3:
            continue
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = col_data[(col_data < lower) | (col_data > upper)]
        for idx, val in outliers.items():
            anomalies.append({
                "column": col,
                "index": int(idx),
                "value": float(val),
                "lower_bound": round(float(lower), 2),
                "upper_bound": round(float(upper), 2),
                "type": "iqr"
            })

    return anomalies

def run_anomaly_detection(df: pd.DataFrame) -> dict:
    """Run full anomaly detection"""
    print("🔍 Running anomaly detection...")

    zscore_anomalies = detect_zscore_anomalies(df)
    iqr_anomalies = detect_iqr_anomalies(df)

    all_anomalies = zscore_anomalies + iqr_anomalies

    # Remove duplicates by column+index
    seen = set()
    unique_anomalies = []
    for a in all_anomalies:
        key = f"{a['column']}-{a['index']}"
        if key not in seen:
            seen.add(key)
            unique_anomalies.append(a)

    print(f"✅ Found {len(unique_anomalies)} anomalies")

    return {
        "total_anomalies": len(unique_anomalies),
        "anomalies": unique_anomalies,
        "columns_checked": list(df.select_dtypes(include="number").columns),
        "rows_checked": len(df)
    }
