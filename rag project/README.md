# Local RAG Document Assistant

This project is a Retrieval-Augmented Generation (RAG) system that allows you to chat with your PDF documents. 

## Model Architecture & Privacy (No External APIs)
This project is built entirely with **local models**, meaning your data never leaves your machine. We do not use any external APIs (like OpenAI or Anthropic). 
- **LLM (Language Model):** We use a local model named **`tinyllama`** which is served locally on your machine via **Ollama**.
- **Embeddings Model:** We use **`sentence-transformers/all-MiniLM-L6-v2`** (via HuggingFace) to generate vector embeddings locally.

## Tech Stack & Libraries
- **LangChain & PyMuPDF (`pymupdf`)**: Used for reading PDF documents and splitting text into chunks.
- **FAISS (`faiss-cpu`)**: A local vector database created by Facebook for fast semantic similarity search.
- **BM25 (`rank_bm25`)**: Used for keyword-based search. Combined with FAISS, this creates a robust **Hybrid Search** retriever.
- **FastAPI & Uvicorn**: Used to build and serve the backend REST API (`app.py`).
- **Streamlit**: Used to build the interactive web-based chat UI (`ui.py`).
- **Ollama Python Client (`ollama`)**: Connects our Python code to the local TinyLlama model.

---

## Prerequisites
1. Download and install Ollama on your computer.
2. Open a terminal and download the TinyLlama model by running:
   ```bash
   ollama pull tinyllama
   ```
3. Create a folder named `data` in the project root and place your PDF files inside it.

## Installation
Install the required Python libraries using pip:
```bash
pip install fastapi uvicorn streamlit langchain langchain-community langchain-text-splitters pymupdf sentence-transformers faiss-cpu rank_bm25 requests ollama
```

---

## How to Run the Project

You will need to open **three separate terminal windows** to run the different parts of this system.

### Step 1: Ingest the Documents (Terminal 1)
Before asking questions, you need to read the PDFs and create the vector database. In your first terminal, run:
```bash
python ingest.py
```
*Note: You only need to run this command once, or whenever you add/remove PDFs in the `data` folder.*

### Step 2: Start the Backend API (Terminal 2)
Open a **second terminal window**, navigate to the project folder, and start the FastAPI backend:
```bash
uvicorn app:app --reload
```
*This will start a local server at `http://127.0.0.1:8000`. Keep this terminal running.*

### Step 3: Start the User Interface (Terminal 3)
Open a **third terminal window**, navigate to the project folder, and start the Streamlit frontend:
```bash
streamlit run ui.py
```
*This command will automatically open a new tab in your web browser with the chat interface. You can now start asking questions about your documents!*