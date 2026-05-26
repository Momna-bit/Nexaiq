from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv("../../.env")

CONN_STR = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER", "datasets")

def get_blob_client():
    return BlobServiceClient.from_connection_string(CONN_STR)

def upload_file(file_bytes: bytes, org_id: str, filename: str) -> str:
    """Upload file to org-specific container and return blob URL"""
    client = get_blob_client()
    container_name = f"org-{org_id}"

    # Create container for this org if it doesn't exist
    try:
        client.create_container(container_name)
    except Exception:
        pass  # Container already exists

    # Upload the file
    blob_client = client.get_blob_client(
        container=container_name,
        blob=filename
    )
    blob_client.upload_blob(file_bytes, overwrite=True)

    return blob_client.url

def delete_file(org_id: str, filename: str):
    """Delete a file from blob storage"""
    client = get_blob_client()
    container_name = f"org-{org_id}"
    blob_client = client.get_blob_client(
        container=container_name,
        blob=filename
    )
    blob_client.delete_blob()

def list_files(org_id: str) -> list:
    """List all files for an org"""
    client = get_blob_client()
    container_name = f"org-{org_id}"
    try:
        container_client = client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]
    except Exception:
        return []
