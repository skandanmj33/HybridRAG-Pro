from rank_bm25 import BM25Okapi
import numpy as np
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load vector DB
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Load chunks again (important)
from ingest import load_documents, split_documents

docs = load_documents()
chunks = split_documents(docs)

# Prepare BM25
tokenized_chunks = [doc.page_content.split() for doc in chunks]
bm25 = BM25Okapi(tokenized_chunks)

# BM25 search
def bm25_search(query, k=5):
    scores = bm25.get_scores(query.split())
    top_n = np.argsort(scores)[-k:]
    return [chunks[i] for i in top_n]

# Hybrid search
def hybrid_search(query, k=5):
    vector_results = db.similarity_search(query, k=k)
    bm25_results = bm25_search(query, k=k)

    # Combine results
    combined = vector_results + bm25_results

    # Remove duplicates
    unique_docs = list({doc.page_content: doc for doc in combined}.values())

    return unique_docs[:k]

if __name__ == "__main__":
    query = "What is cloud computing?"
    results = hybrid_search(query)

    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:\n")
        print(doc.page_content[:300])