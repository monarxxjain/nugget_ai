from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from kb.preprocess import extract_docs
from utils.logger import get_logger
from config.rag_config import (
    QDRANT_COLLECTION_NAME,
    EMBEDDING_MODEL,
    QDRANT_EMBEDDING_LOCAL_PATH,
)

# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()
logger = get_logger()


def build_index():
    logger.info("[+] Loading documents...")
    docs = extract_docs()

    logger.info("[+] Initializing embeddings...")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    logger.info("[+] Connecting to Qdrant...")
    client = QdrantClient(path=QDRANT_EMBEDDING_LOCAL_PATH)

    logger.info("[+] Creating collection...")
    if client.collection_exists(collection_name=QDRANT_COLLECTION_NAME):
        logger.info(
            f"[!] Collection {QDRANT_COLLECTION_NAME} already exists. Deleting it..."
        )
        client.delete_collection(collection_name=QDRANT_COLLECTION_NAME)
    client.create_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )

    logger.info("[+] Inserting vectors...")

    vector_store = QdrantVectorStore(
        client=client,
        embedding=embeddings,
        collection_name=QDRANT_COLLECTION_NAME,
    )

    batch_size = 10
    for i in range(0, len(docs), batch_size):
        batch = docs[i : i + batch_size]
        try:
            vector_store.add_documents(documents=batch)
            logger.info(
                f"[✓] Successfully inserted batch {i // batch_size + 1} ({len(batch)} docs)"
            )
        except Exception as e:
            logger.error(f"[!] Failed batch {i // batch_size + 1}: {e}")
            continue

    logger.info("[✓] Indexing complete!")


if __name__ == "__main__":
    build_index()
