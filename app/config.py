import os
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


def _get_secret(key: str) -> str | None:
    """Read a secret from env first, then Streamlit secrets."""
    value = os.getenv(key)
    if value:
        return value

    try:
        import streamlit as st

        secret_value = st.secrets.get(key)
        if secret_value:
            return str(secret_value)
    except Exception:
        return None

    return None


OPENAI_API_KEY = _get_secret("OPENAI_API_KEY")

_default_chroma = _PROJECT_ROOT / "chroma"
CHROMA_PATH = os.getenv("CHROMA_PATH", str(_default_chroma))
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "kent_university_docs")

_default_ingest_data = _PROJECT_ROOT / "data" / "kent-university.md"
INGEST_DATA_PATH = Path(os.getenv("INGEST_DATA_PATH", str(_default_ingest_data)))
