"""
NexaIQ Vector Store — ChromaDB
Stores document embeddings for RAG pipeline
"""

import chromadb
from chromadb.config import Settings
import os

CHROMA_PATH = os.path.expanduser("~/nexaiq/chroma_db")

_client = None

def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
    return _client

def get_collection(org_id: str):
    """Get or create a collection for an org"""
    client = get_chroma_client()
    collection_name = f"org_{org_id[:8].replace('-', '_')}"
    try:
        collection = client.get_collection(collection_name)
    except:
        collection = client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    return collection

def add_documents(org_id: str, texts: list, metadatas: list, ids: list):
    """Add documents to the vector store"""
    collection = get_collection(org_id)
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Added {len(texts)} documents to ChromaDB for org {org_id[:8]}")

def search_documents(org_id: str, query: str, n_results: int = 3) -> list:
    """Search for relevant documents"""
    collection = get_collection(org_id)
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    documents = results["documents"][0] if results["documents"] else []
    metadatas = results["metadatas"][0] if results["metadatas"] else []
    distances = results["distances"][0] if results["distances"] else []
    return [
        {
            "text": doc,
            "metadata": meta,
            "relevance": round(1 - dist, 3)
        }
        for doc, meta, dist in zip(documents, metadatas, distances)
    ]

def delete_collection(org_id: str):
    """Delete all documents for an org"""
    client = get_chroma_client()
    collection_name = f"org_{org_id[:8].replace('-', '_')}"
    try:
        client.delete_collection(collection_name)
        print(f"Deleted collection for org {org_id[:8]}")
    except:
        pass

def get_collection_stats(org_id: str) -> dict:
    """Get stats about the collection"""
    collection = get_collection(org_id)
    count = collection.count()
    return {
        "org_id": org_id[:8],
        "document_count": count,
        "collection_name": f"org_{org_id[:8].replace('-', '_')}"
    }
