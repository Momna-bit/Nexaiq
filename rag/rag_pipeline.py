"""
NexaIQ RAG Pipeline
Processes documents and answers questions
"""

from openai import OpenAI
from vector_store import add_documents, search_documents, get_collection_stats
import os
import uuid
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    with open(os.path.expanduser("~/nexaiq/.env")) as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY="):
                OPENAI_API_KEY = line.strip().split("=", 1)[1]

client = OpenAI(api_key=OPENAI_API_KEY)

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks

def ingest_document(org_id: str, text: str, doc_name: str, doc_type: str = "text") -> dict:
    """Ingest a document into the vector store"""
    print(f"Ingesting document: {doc_name}")
    chunks = chunk_text(text)
    print(f"Split into {len(chunks)} chunks")
    ids = [f"{org_id[:8]}_{doc_name}_{i}_{str(uuid.uuid4())[:8]}" for i in range(len(chunks))]
    metadatas = [
        {
            "doc_name": doc_name,
            "doc_type": doc_type,
            "chunk_index": str(i),
            "org_id": org_id[:8]
        }
        for i in range(len(chunks))
    ]
    add_documents(
        org_id=org_id,
        texts=chunks,
        metadatas=metadatas,
        ids=ids
    )
    stats = get_collection_stats(org_id)
    print(f"Vector store now has {stats['document_count']} chunks")
    return {
        "doc_name": doc_name,
        "chunks_created": len(chunks),
        "total_chunks_in_store": stats["document_count"]
    }

def answer_question(org_id: str, question: str, n_context: int = 3) -> dict:
    """Answer a question using RAG"""
    print(f"Question: {question}")
    relevant_docs = search_documents(org_id, question, n_results=n_context)
    if not relevant_docs:
        return {
            "question": question,
            "answer": "No relevant documents found. Please upload some documents first.",
            "sources": [],
            "context_used": 0
        }
    context = "\n\n".join([
        f"[Source: {doc['metadata']['doc_name']}]\n{doc['text']}"
        for doc in relevant_docs
    ])
    prompt = f"""You are a helpful AI assistant for NexaIQ, a B2B data intelligence platform.
Answer the question based ONLY on the provided context below.
If the answer is not in the context, say "I don't have enough information to answer this."

Context:
{context}

Question: {question}

Answer:"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful business intelligence assistant. Answer questions based on the provided context only."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.1
    )
    answer = response.choices[0].message.content
    sources = list(set([doc["metadata"]["doc_name"] for doc in relevant_docs]))
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "context_used": len(relevant_docs),
        "relevant_chunks": [
            {
                "text": doc["text"][:200] + "...",
                "source": doc["metadata"]["doc_name"],
                "relevance": doc["relevance"]
            }
            for doc in relevant_docs
        ]
    }

if __name__ == "__main__":
    ORG_ID = "e22043da-16d5-49b9-b6da-5765a5e7edd9"

    print("Testing NexaIQ RAG Pipeline...\n")

    # Ingest sample business documents
    doc1 = """
    NexaIQ Q3 2024 Revenue Report
    Total Revenue: $2.4 million, up 23% from Q2.
    Key drivers: Enterprise tier grew 45%, new customers in EU region.
    Churn rate decreased to 3.2% from 4.8% in Q2.
    Top performing product: AI Anomaly Detection module.
    Customer satisfaction score: 4.7/5.0.
    Headcount: 42 employees, 8 new hires in engineering.
    """

    doc2 = """
    NexaIQ Product Roadmap 2025
    Q1 2025: Launch RAG pipeline for document Q&A.
    Q2 2025: Release LangGraph autonomous agents.
    Q3 2025: Expand to APAC market, new Singapore office.
    Q4 2025: IPO preparation begins.
    Key focus areas: AI/ML capabilities, enterprise security, compliance.
    Target ARR by end of 2025: $12 million.
    """

    doc3 = """
    NexaIQ Customer Success Stories
    Acme Corp: Reduced data analysis time by 70% using AutoML.
    Global Bank: Detected $2M fraud using anomaly detection.
    RetailCo: Increased revenue forecast accuracy to 94%.
    TechStartup: Replaced 3 analysts with NexaIQ platform.
    Average ROI reported by customers: 340% in first year.
    """

    print("Ingesting documents...")
    ingest_document(ORG_ID, doc1, "Q3_Revenue_Report", "report")
    ingest_document(ORG_ID, doc2, "Product_Roadmap_2025", "roadmap")
    ingest_document(ORG_ID, doc3, "Customer_Success_Stories", "case_studies")

    print("\nAsking questions...\n")

    questions = [
        "What was the revenue in Q3 2024?",
        "When will LangGraph agents be released?",
        "What ROI do customers report?",
        "What is the churn rate?"
    ]

    for q in questions:
        result = answer_question(ORG_ID, q)
        print(f"Q: {result['question']}")
        print(f"A: {result['answer']}")
        print(f"Sources: {result['sources']}")
        print()
