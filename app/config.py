import os
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

_default_chroma = _PROJECT_ROOT / "chroma"
CHROMA_PATH = os.getenv("CHROMA_PATH", str(_default_chroma))
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "kent_university_docs")

_default_ingest_data = _PROJECT_ROOT / "data" / "kent-university.md"
INGEST_DATA_PATH = Path(os.getenv("INGEST_DATA_PATH", str(_default_ingest_data)))
