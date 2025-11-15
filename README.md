# Ambedkar Q&A System -- Setup Guide

This project uses **LangChain + ChromaDB + FAISS + Ollama (Mistral 7B)**
to create a local RAG-based Q&A system.

------------------------------------------------------------------------

## ✅ 1. Install Ollama & Pull Model

Make sure Ollama is installed on your system.

Then pull the Mistral model:

    ollama pull mistral

------------------------------------------------------------------------

## ✅ 2. Clone the Repository

    git clone https://github.com/PRM710/BR_LLM.git
    cd BR_LLM

------------------------------------------------------------------------

## ✅ 3. Backend Setup

### ▶ Step 1 --- Go to the backend folder

    cd backend

### ▶ Step 2 --- Create Virtual Environment

    python -m venv venv

### ▶ Step 3 --- Activate venv

**Windows:**

    venv\Scripts\activate

**Mac/Linux:**

    source venv/bin/activate

------------------------------------------------------------------------

## ✅ 4. Install Required Python Dependencies

Install EXACT versions and packages in this order:

    pip install langchain==0.1.16
    pip install langchain-community
    pip install langchain-text-splitters
    pip install chromadb
    pip install sentence-transformers
    pip install ollama
    pip install faiss-cpu

------------------------------------------------------------------------

## ✅ 5. Run the Backend Server

Make sure you stay inside the **backend folder**, then run:

    python server.py

Your API will start at:

    http://127.0.0.1:8000

------------------------------------------------------------------------

## 🚀 You're Ready!

Use the API in your frontend (React) to send questions to:

    POST /ask

With body:

``` json
{ "question": "your question here" }
```

------------------------------------------------------------------------
