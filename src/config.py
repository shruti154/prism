import os
from dotenv import load_dotenv

load_dotenv()

# API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Paths — absolute so they work from anywhere
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")
DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "documents")

# Models
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
LLM_MODEL = "claude-sonnet-4-20250514"

# RAG settings
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 10

# News settings
NEWS_LANGUAGE = "en"
NEWS_PAGE_SIZE = 5