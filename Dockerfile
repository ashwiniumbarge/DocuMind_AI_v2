# ============================================================
# DocuMind AI v2 - Streamlit hybrid RAG application
# Build:  docker build -t documind-ai .
# Run:    docker run -p 8501:8501 --env-file .env documind-ai
# ============================================================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/app/cache/huggingface

WORKDIR /app

# curl is only used by the container health check
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# CPU-only PyTorch first (keeps the image far smaller than the default CUDA build)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install -r requirements.txt

# Download the embedding and re-ranker models at build time so the first request is fast.
# Model names match EMBEDDING_MODEL and RERANKER_MODEL in core/config.py.
RUN python -c "from sentence_transformers import SentenceTransformer, CrossEncoder; \
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2'); \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

COPY . .

# Folders the app writes to (core/config.py also creates them on start)
RUN mkdir -p uploads vectorstores database logs exports cache assets

# Run as a non-root user
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# GOOGLE_API_KEY is passed at runtime (never baked into the image)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
