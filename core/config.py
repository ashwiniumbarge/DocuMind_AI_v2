"""
============================================================
DocuMind AI v2
Configuration File
============================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

# ============================================================
# Project Directories
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / "uploads"
VECTORSTORE_DIR = BASE_DIR / "vectorstores"
DATABASE_DIR = BASE_DIR / "database"
LOG_DIR = BASE_DIR / "logs"
EXPORT_DIR = BASE_DIR / "exports"
CACHE_DIR = BASE_DIR / "cache"
ASSETS_DIR = BASE_DIR / "assets"

# Create folders automatically
for directory in [
    UPLOAD_DIR,
    VECTORSTORE_DIR,
    DATABASE_DIR,
    LOG_DIR,
    EXPORT_DIR,
    CACHE_DIR,
    ASSETS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================
# Database
# ============================================================

DATABASE_PATH = DATABASE_DIR / "documind.db"

# ============================================================
# Google Gemini
# ============================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

LLM_MODEL = "models/gemini-3.5-flash"

TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 2048

# ============================================================
# Embedding Model
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ============================================================
# Reranker
# ============================================================

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ============================================================
# Chunking
# ============================================================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ============================================================
# Retrieval
# ============================================================

TOP_K = 5

SIMILARITY_THRESHOLD = 0.70

USE_BM25 = True

USE_RERANKER = True

# ============================================================
# Conversation Memory
# ============================================================

MAX_CHAT_HISTORY = 10

# ============================================================
# Supported File Types
# ============================================================

SUPPORTED_EXTENSIONS = [
    ".pdf",
]

MAX_FILE_SIZE_MB = 50

# ============================================================
# Logging
# ============================================================

LOG_FILE = LOG_DIR / "documind.log"

LOG_LEVEL = "INFO"

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "DocuMindAI | "
    "%(message)s"
)

# ============================================================
# Streamlit
# ============================================================

APP_TITLE = "DocuMind AI v2"

APP_ICON = "📚"

# ============================================================
# Application Settings
# ============================================================

APP_VERSION = "2.0.0"

DEBUG = True