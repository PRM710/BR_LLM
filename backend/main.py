"""
Ambedkar Q&A RAG System
Uses:
- LangChain
- ChromaDB
- HuggingFaceEmbeddings
- Ollama (Mistral)

This file builds:
1. Vector store
2. Retrieval QA chain

FastAPI imports qa_chain from here.
"""

import os
import argparse

# Updated imports
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

# ==== CONFIG ====
SPEECH_FILE = "speech.txt"
PERSIST_DIR = "./chroma_db"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


# ============================
# Build Vector Database
# ============================
def build_vectorstore(force_rebuild=False):
    """Load or build Chroma DB"""

    if os.path.exists(PERSIST_DIR) and not force_rebuild:
        print("Loading existing ChromaDB...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        return Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings
        )

    print("Building new ChromaDB...")

    if not os.path.exists(SPEECH_FILE):
        raise FileNotFoundError("speech.txt not found!")

    loader = TextLoader(SPEECH_FILE, encoding="utf-8")
    docs = loader.load()

    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        keep_separator=True
    )

    chunks = splitter.split_documents(ddocs := docs)
    print(f"Created {len(chunks)} chunks")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    vectordb.persist()
    print("ChromaDB saved!")

    return vectordb


# ============================
# Build QA Chain
# ============================
def build_qa_chain(vectordb):
    llm = Ollama(model="mistral")

    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    return qa


# ==============================
# CREATE FOR FASTAPI GLOBALLY
# ==============================

print("Initializing vector DB and QA chain...")
vectordb = build_vectorstore(force_rebuild=False)
qa_chain = build_qa_chain(vectordb)
print("RAG system ready.")


# ============================
# Optional CLI Mode
# ============================
def cli_loop():
    print("\n=== Ambedkar Q&A System ===")
    print("Ask anything about the speech.")
    print("Type 'exit' to quit.\n")

    while True:
        q = input("Q: ")

        if q.lower() in ["exit", "quit"]:
            break

        try:
            ans = qa_chain.run(q)
            print("\n> Answer:", ans)
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args()

    if args.rebuild:
        print("Rebuilding vector DB...")
        vectordb2 = build_vectorstore(force_rebuild=True)
        qa_chain2 = build_qa_chain(vectordb2)
        cli_loop()
    else:
        cli_loop()
