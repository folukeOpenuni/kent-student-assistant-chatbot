# Kent Student Assistant Chatbot

AI-powered Streamlit chatbot for University of Kent student support guidance.  
The app uses retrieval-augmented generation (RAG) with OpenAI embeddings and ChromaDB over curated Kent documentation.

## Tech Stack

- Streamlit
- OpenAI API
- ChromaDB
- Python dotenv

## Project Structure

- `app/main.py` - Streamlit UI entrypoint
- `app/prompts.py` - LLM prompt template and response generation
- `app/retrieval.py` - Embedding + Chroma retrieval logic (auto-ingests on first run if collection is missing)
- `app/ingest.py` - Document chunking + indexing into Chroma
- `app/config.py` - Environment/secrets config
- `data/` - Source markdown knowledge files

## Run Locally

1. Create and activate a virtual environment.
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Add your API key in `.env`:
   - `OPENAI_API_KEY=your_key_here`
4. Start the app:
   - `streamlit run app/main.py`

## Streamlit Cloud Deployment

1. Push this repo to GitHub.
2. Create a new app on Streamlit Community Cloud.
3. Set the main file path to:
   - `app/main.py`
4. In app **Secrets**, add:
   - `OPENAI_API_KEY = "your_key_here"`
5. Deploy.

Notes:
- `requirements.txt` is used for dependency installation.
- If the Chroma collection does not exist on first run, the app automatically ingests and builds it.

## Configuration

Optional environment variables:

- `CHROMA_PATH` (default: `./chroma`)
- `CHROMA_COLLECTION_NAME` (default: `kent_university_docs`)
- `INGEST_DATA_PATH` (default: `./data/kent-university.md`)
