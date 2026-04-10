from fastapi import FastAPI
from pydantic import BaseModel
from generator import generate_answer

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "RAG API is running 🚀"}

@app.post("/ask")
def ask_question(request: QueryRequest):
    answer = generate_answer(request.question)
    return {
        "question": request.question,
        "answer": answer
    }