import pandas as pd
import io
from azure.storage.blob import BlobServiceClient
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv("../../.env")

DATABASE_URL = os.getenv("DATABASE_URL")
CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

engine = create_engine(DATABASE_URL)

def read_csv_from_blob(org_id: str, filename: str) -> pd.DataFrame:
    """Read CSV file from Azure Blob Storage into DataFrame"""
    client = BlobServiceClient.from_connection_string(CONN_STR)
    container_name = f"org-{org_id}"
    blob_client = client.get_blob_client(
        container=container_name,
        blob=filename
    )
    blob_data = blob_client.download_blob().readall()
    return pd.read_csv(io.BytesIO(blob_data))

def save_raw(df: pd.DataFrame, org_id: str, dataset_id: str):
    """Save raw data as-is to raw table"""
    df = df.copy()
    df["org_id"] = org_id
    df["dataset_id"] = dataset_id
    df.to_sql(
        "raw_data",
        engine,
        if_exists="append",
        index=False
    )
    print(f"✅ RAW: saved {len(df)} rows")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the data"""
    # Remove duplicates
    df = df.drop_duplicates()
    # Remove rows where all values are null
    df = df.dropna(how="all")
    # Fill numeric nulls with median
    for col in df.select_dtypes(include="number").columns:
        df[col] = df[col].fillna(df[col].median())
    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    print(f"✅ CLEAN: {len(df)} rows after cleaning")
    return df

def save_clean(df: pd.DataFrame, org_id: str, dataset_id: str):
    """Save cleaned data"""
    df = df.copy()
    df["org_id"] = org_id
    df["dataset_id"] = dataset_id
    df.to_sql(
        "clean_data",
        engine,
        if_exists="append",
        index=False
    )
    print(f"✅ CLEAN saved to database")

def build_mart(df: pd.DataFrame, org_id: str, dataset_id: str):
    """Build summary mart table"""
    mart = {
        "org_id": org_id,
        "dataset_id": dataset_id,
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "numeric_columns": len(df.select_dtypes(include="number").columns),
        "null_count": int(df.isnull().sum().sum()),
        "columns": ",".join(df.columns.tolist())
    }
    mart_df = pd.DataFrame([mart])
    mart_df.to_sql(
        "mart_summary",
        engine,
        if_exists="append",
        index=False
    )
    print(f"✅ MART: summary saved")
    return mart

def run_pipeline(org_id: str, dataset_id: str, blob_filename: str):
    """Run full RAW -> CLEAN -> MART pipeline"""
    print(f"🚀 Starting pipeline for dataset {dataset_id}")

    # Step 1 - Read from blob
    print("📥 Reading from Azure Blob Storage...")
    df = read_csv_from_blob(org_id, blob_filename)

    # Step 2 - Save RAW
    save_raw(df, org_id, dataset_id)

    # Step 3 - Clean
    df_clean = clean_data(df)

    # Step 4 - Save CLEAN
    save_clean(df_clean, org_id, dataset_id)

    # Step 5 - Build MART
    mart = build_mart(df_clean, org_id, dataset_id)

    print(f"✅ Pipeline complete!")
    return mart
