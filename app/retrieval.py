import chromadb
from config import CHROMA_COLLECTION_NAME, CHROMA_PATH, OPENAI_API_KEY
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


class KnowledgeRetriever:
    """Encapsulates embedding and Chroma retrieval behavior."""

    def __init__(
        self,
        *,
        api_key: str = OPENAI_API_KEY,
        chroma_path: str = CHROMA_PATH,
        collection_name: str = CHROMA_COLLECTION_NAME,
        embedding_model: str = EMBEDDING_MODEL,
    ):
        self.client = OpenAI(api_key=api_key)
        self.chroma_path = chroma_path
        self.collection_name = collection_name
        self.embedding_model = embedding_model

    def get_chroma_collection(self):
        """Return the indexed collection from disk. Run ingest first if missing."""
        client = chromadb.PersistentClient(path=self.chroma_path)
        return client.get_collection(name=self.collection_name)

    def embed_query(self, text: str) -> list[float]:
        """Embed a single user question for similarity search."""
        question = text.strip()
        if not question:
            raise ValueError("Query text must be non-empty")
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=question,
        )
        return response.data[0].embedding

    def retrieve(self, query: str, n_results: int = 3) -> list[dict]:
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
        embedding = self.embed_query(query)
        collection = self.get_chroma_collection()
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


default_retriever = KnowledgeRetriever()


def retriever(query: str, n_results: int = 3) -> list[dict]:
    """Backward-compatible helper that proxies to ``KnowledgeRetriever.retrieve``."""
    return default_retriever.retrieve(query, n_results=n_results)
