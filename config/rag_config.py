from pathlib import Path

RAW_JSON_DIR = Path("data/raw_json")
PROCESSED_JSON_DIR = Path("data/processed_json")

# EMBEDDING_MODEL = (
#     "models/gemini-embedding-exp-03-07"
# )
EMBEDDING_MODEL = "BAAI/bge-m3"

GENERATION_MODEL = "gemini-2.0-flash"
TEMPERATURE = 0.2
TOP_P = 0.9

# Qdrant Config
# QDRANT_HOST = "localhost"  # or 'qdrant://localhost:6333' if using Qdrant client
# QDRANT_PORT = 6333
QDRANT_COLLECTION_NAME = "restaurant_knowledge_base"
QDRANT_EMBEDDING_LOCAL_PATH = "/tmp/langchain_qdrant"
TOP_K = 5
