# Connect and query the vector store (same paths/names as ingest).

import chromadb
from config import CHROMA_COLLECTION_NAME, CHROMA_PATH, OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)
EMBEDDING_MODEL = "text-embedding-3-small"


def get_chroma_collection():
    """Return the indexed collection from disk. Run ingest first if missing."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_collection(name=CHROMA_COLLECTION_NAME)


def embed_query(text: str) -> list[float]:
    """Embed a single user question for similarity search."""
    question = text.strip()
    if not question:
        raise ValueError("Query text must be non-empty")
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=question,
    )
    return response.data[0].embedding


def retriever(query: str, n_results: int = 3) -> list[dict]:
    """
    Embed ``query``, run similarity search, return ranked chunks.

    Each item: ``id``, ``document`` (text), ``metadata`` (e.g. section), ``distance``
    (lower is closer for L2; Chroma default distance).

    Args:
        query: User question (natural language).
        n_results: How many chunks to return (best matches first).

    Returns:
        List of dicts with keys ``id``, ``document``, ``metadata``, ``distance``.
    """
    embedding = embed_query(query)
    collection = get_chroma_collection()
    batch = collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    ids = batch["ids"][0]
    documents = batch["documents"][0]
    metadatas = batch["metadatas"][0]
    distances = batch["distances"][0]
    return [
        {
            "id": ids[i],
            "document": documents[i],
            "metadata": metadatas[i],
            "distance": distances[i],
        }
        for i in range(len(ids))
    ]
