from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from main import build_vectorstore, build_qa_chain

# --- Initialize ---
print("Initializing vector DB and QA chain...")
vectordb = build_vectorstore(force_rebuild=False)
qa_chain = build_qa_chain(vectordb)
print("RAG system ready.")

app = FastAPI()

# --- CORS FIX (VERY IMPORTANT) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # React frontend allowed
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(q: Question):
    answer = qa_chain.run(q.question)
    return {"answer": answer}
