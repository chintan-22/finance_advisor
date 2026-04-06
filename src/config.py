import os
from dotenv import load_dotenv

load_dotenv()

FMP_API_KEY = os.environ.get("FMP_API_KEY")
NEWSAPI_API_KEY = os.environ.get("NEWSAPI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

# Chroma persist directories
CHROMA_PERSIST_DIR = os.environ.get("CHROMA_PERSIST_DIR", "docs/chroma/")
CHROMA_PERSIST_DIR_RAG = os.environ.get("CHROMA_PERSIST_DIR_RAG", "docs/chroma_rag/")
