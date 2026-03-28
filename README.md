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

## Demo Test Questions

Here are 10 ready-made questions you can ask the chatbot to test functionality against the project brief:

1. **Admissions & Enrollment**  
   "I've just received an offer to study Computer Science. What are the next steps to confirm my place?"

2. **Assessment & Deadlines**  
   "When is the deadline to withdraw from a module without it affecting my final grade?"

3. **Wellbeing Support**  
   "I've been feeling really overwhelmed lately. Who can I speak to for mental health support on campus?"

4. **General Enquiries**  
   "I've lost my student ID card. How do I get a replacement and is there a temporary one I can use?"

5. **Technical Support**  
   "I can't log into the Virtual Learning Environment (VLE). It says my password is incorrect even after resetting it."

6. **International Student Support**  
   "As an international student, what documents do I need to provide to prove my right to study for the next semester?"

7. **Financial & Fees**  
   "I'm worried I won't be able to pay my tuition fees by the installment deadline. What options do I have?"

8. **Procedural (Redirection)**  
   "How do I apply for extenuating circumstances for an exam I missed last week?"

9. **Career & Progression**  
   "I'm unsure which optional modules to pick for next year to qualify for a placement year. Can someone advise me?"

10. **Critical Scenario**  
    "I am having a technical issue with the chatbot itself and cannot find the contact details for the IT service desk."

## Known Limitations + Next Steps

Current limitations:

- No live University API integration yet (knowledge is sourced from local, curated documents).
- Basic retrieval and reranking strategy (top-k vector search only, without advanced hybrid reranking).
- Single-turn memory (conversation context is not persisted across longer multi-turn sessions).
- Limited source coverage (currently focused on selected Kent guidance documents).
- No built-in evaluation dashboard for tracking answer quality over time.

Planned next steps:

- Add live integrations for key university services where APIs are available.
- Improve retrieval quality with hybrid search and stronger reranking pipelines.
- Introduce lightweight conversational memory with clear guardrails.
- Expand and version the knowledge base with scheduled re-indexing.
- Add automated evals (groundedness, citation quality, and helpfulness) before deployment.
