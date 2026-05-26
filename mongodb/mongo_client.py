from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

MONGODB_URI = "mongodb+srv://nexaiq:nexaiq123@nexaiq-cluster.vr9vpku.mongodb.net/?appName=nexaiq-cluster"

_client = None

def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI)
    return _client

def get_db(db_name: str = "nexaiq"):
    return get_client()[db_name]

def test_connection():
    try:
        client = get_client()
        client.admin.command('ping')
        print("MongoDB Atlas connected successfully!")
        return True
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
