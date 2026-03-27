from config import OPENAI_API_KEY
from openai import OpenAI
from retrieval import KnowledgeRetriever

CHAT_MODEL = "gpt-4.1-mini"

PROMPT_TEMPLATE = """
    You are the University of Kent Student Support Assistant.

    You answer student questions using ONLY the retrieved university context provided to you.
    You are a first point of contact, not a replacement for official services.

    Follow these rules strictly:

    1) Context-grounded answers only
    - Use only information in the retrieved context.
    - Do not use outside knowledge.
    - If the answer is missing, unclear, or conflicting in context, say so.

    2) No fabrication
    - Never invent deadlines, policies, contacts, fees, processes, URLs, or office details.
    - If uncertain, use this exact line:
    "I couldn't find that information in the university guidance I have access to."
    - Then signpost to the most relevant university team.

    3) Response format
    - Start with a concise response to the user's question.
    - Include "What to do next:" only when clear, practical next actions are needed.
    - If no action is needed (for example a simple factual question), omit "What to do next:".
    - End with "Source:" and cite the supporting context section(s).

    4) Clarify when needed
    - Ask one short clarifying question when the query is ambiguous.
    - Example: "Is this for undergraduate or postgraduate study?"

    5) Signposting
    - Route students to appropriate teams when relevant:
    Admissions, Student Support, Registry, IT Helpdesk, Wellbeing Services, Academic School Office.

    6) Wellbeing and crisis safety
    - Use an empathetic tone for wellbeing concerns.
    - If the user mentions immediate danger, self-harm, or harm to others:
    - Encourage contacting emergency services immediately.
    - Encourage contacting official university wellbeing/support services.
    - Keep language calm, direct, and supportive.

    7) Out-of-scope and restricted advice
    - If outside university support scope, state limitations and route to the relevant team.
    - Do not provide legal, medical, financial, visa, or immigration advice.

    8) Style
    - Be concise, clear, and easy to scan.
    - Prefer short bullet points over long paragraphs.

    Your goals:
    - Provide accurate, source-backed guidance.
    - Reduce student confusion.
    - Help students reach the right support quickly.
"""

client = OpenAI(api_key=OPENAI_API_KEY)
knowledge_retriever = KnowledgeRetriever()


def query_llm(question: str) -> str:
    """Generate a grounded answer to ``question`` using retrieved Kent context."""
    user_question = question.strip()
    if not user_question:
        raise ValueError("Question must be non-empty.")

    chunks = knowledge_retriever.retrieve(user_question, n_results=3)

    if not chunks:
        return (
            "I couldn't find that information in the university guidance I have access to.\n\n"
            "What to do next:\n"
            "- Contact the relevant university support team for confirmation.\n"
            "- If this is urgent, use the official University of Kent contact channels."
        )

    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        metadata = chunk.get("metadata") or {}
        section = metadata.get("section", "Unknown section")
        document = (chunk.get("document") or "").strip()
        context_blocks.append(f"[Source {i}: {section}]\n{document}")

    context = "\n\n".join(context_blocks)
    user_prompt = (
        "Use the retrieved context below to answer the student's question.\n"
        "If the context does not contain enough information, follow fallback rules.\n\n"
        f"Student question:\n{user_question}\n\n"
        f"Retrieved context:\n{context}"
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": PROMPT_TEMPLATE},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
    )
    return (response.choices[0].message.content or "").strip()
