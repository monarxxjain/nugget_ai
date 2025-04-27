from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from config.rag_config import (
    QDRANT_COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
    QDRANT_EMBEDDING_LOCAL_PATH,
)
from dotenv import load_dotenv
from utils.logger import get_logger

load_dotenv()

logger = get_logger()

logger.info("[+] Loading Qdrant client...")
client = QdrantClient(path=QDRANT_EMBEDDING_LOCAL_PATH)

logger.info("[+] Initializing embeddings...")
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

db = QdrantVectorStore(
    client=client, collection_name=QDRANT_COLLECTION_NAME, embedding=embeddings
)


def get_relevant_chunks(query: str) -> list[str]:
    logger.info(f"[+] Searching for relevant chunks for query: {query}")

    results = db.similarity_search(query, k=TOP_K)

    logger.debug(f"[+] Results: {results}")
    logger.info(f"[✓] Retrieved {len(results)} relevant chunks")
    return [doc.page_content for doc in results]
