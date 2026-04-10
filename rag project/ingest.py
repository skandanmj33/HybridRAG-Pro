from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

# Step 1: Load all PDFs from data folder
def load_documents():
    docs = []
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            loader = PyMuPDFLoader(f"data/{file}")
            docs.extend(loader.load())
    return docs

# Step 2: Split into chunks
def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)

# Step 3: Create FAISS vector DB
def create_vector_db(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("faiss_index")

    print("✅ Vector DB created successfully!")

# Run everything
if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    create_vector_db(chunks)