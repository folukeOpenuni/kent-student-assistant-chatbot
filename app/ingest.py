import logging
import re

import chromadb
from config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_PATH,
    INGEST_DATA_PATH,
    OPENAI_API_KEY,
)
from openai import OpenAI

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)
_SECTION_PATTERN = re.compile(r"(##\s+\d+\.\s+[A-Za-z ]+)")


def load_markdown():
    return INGEST_DATA_PATH.read_text(encoding="utf-8")


def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def chunk_by_sections(text):
    parts = _SECTION_PATTERN.split(text)
    chunks = []

    preamble = parts[0].strip()
    if preamble:
        chunks.append({"section": "Overview", "content": preamble})

    for i in range(1, len(parts), 2):
        heading = parts[i].strip()
        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        section_name = heading.removeprefix("##").strip()
        chunks.append({"section": section_name, "content": f"{heading}\n\n{content}"})

    if not chunks and text.strip():
        chunks.append({"section": "Document", "content": text.strip()})

    return chunks


def embed_text(texts):
    response = client.embeddings.create(model="text-embedding-3-small", input=texts)

    return [item.embedding for item in response.data]


def build_chroma(chunks, collection_name=CHROMA_COLLECTION_NAME):
    """
    Store markdown chunks in a persistent Chroma DB.

    1. PersistentClient(path=...) -> SQLite + vector index on disk under CHROMA_PATH.
    2. get_or_create_collection(name=...) -> named "table" for this project.
    3. add(ids, embeddings, documents, metadatas) -> one row per chunk.

    Later, query with the same embedding model: collection.query(
        query_embeddings=[...], n_results=5
    ).
    """
    if not chunks:
        logger.warning("No chunks to index; skipping Chroma write")
        return

    documents = [c["content"] for c in chunks]
    metadatas = [{"section": c["section"]} for c in chunks]
    ids = [f"kent-{i}" for i in range(len(chunks))]
    embeddings = embed_text(documents)

    chroma = chromadb.PersistentClient(path=CHROMA_PATH)

    existing = {c.name for c in chroma.list_collections()}
    if collection_name in existing:
        logger.info("Removing existing collection %r", collection_name)
        chroma.delete_collection(collection_name)

    collection = chroma.create_collection(name=collection_name)
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )
    logger.info(
        "Indexed %s chunks into Chroma at %s (collection %r)",
        len(ids),
        CHROMA_PATH,
        collection_name,
    )


def ingest():
    logger.info("Loading %s", INGEST_DATA_PATH)
    text = load_markdown()
    chunks = chunk_by_sections(text)
    logger.info("Split markdown into %s section chunks", len(chunks))
    build_chroma(chunks)
