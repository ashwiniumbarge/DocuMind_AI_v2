# DocuMind AI

A hybrid Retrieval-Augmented Generation (RAG) assistant that lets you upload PDF documents and ask questions in natural language. Answers come only from your documents, with page-level source citations.

## Problem

Finding answers in long PDFs is slow, and general-purpose LLMs can make up information when they have no source. DocuMind retrieves the most relevant passages from your own documents and makes the LLM answer from them only.

## Features

- Upload PDFs and chat with them, with multi-turn conversation memory
- Hybrid retrieval: FAISS semantic search plus BM25 keyword search
- Cross-encoder re-ranking of the retrieved chunks before they reach the LLM
- Page-level source citations and a retrieved-sources viewer
- User login with bcrypt password hashing
- SQLite storage for users, documents and chat history
- Document upload and delete management
- Retrieval vs generation latency tracking
- Logging and modular code structure

## How it works

1. **Ingestion:** text is extracted from each PDF (pypdf), cleaned and split into chunks (1,000 characters, 200 overlap) with source and page metadata.
2. **Indexing:** chunks are embedded with `all-MiniLM-L6-v2` and stored in a separate FAISS index per document.
3. **Retrieval:** the question is searched with FAISS (semantic) and BM25 (keyword). Results are merged and de-duplicated.
4. **Re-ranking:** a cross-encoder (`ms-marco-MiniLM-L-6-v2`) scores the candidates and the top 5 chunks are kept.
5. **Generation:** a grounded prompt (answer only from the context, with a fallback reply when the answer is missing) plus the last few conversation turns is sent to Google Gemini.

## Tech stack

Python, Streamlit, LangChain, FAISS, BM25 (rank-bm25), Sentence-Transformers, Google Gemini API, pypdf, SQLite, bcrypt, Docker

## Project structure

```
app.py        Streamlit entry point
app/          UI components (chat, sidebar, layout)
core/         Config, authentication, database, logging, memory
rag/          PDF processing, embeddings, vector store, retriever, re-ranker, prompt builder, RAG engine
```

## Setup

### Run locally

```bash
git clone https://github.com/ashwiniumbarge/DocuMind_AI_v2.git
cd DocuMind_AI_v2
python -m venv venv
venv\Scripts\activate        # Windows (use: source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`):

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Start the app:

```bash
streamlit run app.py
```

### Run with Docker

```bash
docker compose up --build
```

Then open `http://localhost:8501` in your browser.

## Author

Ashwini Umbarge - [LinkedIn](https://www.linkedin.com/in/ashwini-umbarge-66b063221)
