# kent-student-assistant-chatbot

AI-powered student assistant chatbot for the University of Kent. It uses a FastAPI backend, OpenAI models, and retrieval-augmented generation over curated Kent information to answer questions about student support, general enquiries, and admissions.

## Prototype Spec: University Student Support Chatbot

### 1) Problem Statement
Students often struggle to quickly find accurate information across multiple University web pages (admissions, assessments, deadlines, wellbeing, general enquiries).
This prototype chatbot acts as a first-line support assistant that gives fast, reliable, source-grounded answers and routes uncertain/high-risk queries to official human support channels.

### 2) Goal
Build a working AI chatbot prototype for the University website that:
- Answers common student support questions.
- Cites trusted university content.
- Handles unknowns safely (no guessing).
- Provides escalation links for human help.

### 3) MVP Scope (Phase 1)
In scope (required categories):
- Admissions (requirements, application process, key timelines).
- Assessments (formats, submission basics, policy overview).
- Deadlines (application/assessment-related deadline guidance).
- Wellbeing support (where to get support, emergency/non-emergency contacts).
- General enquiries (contact points, office hours, student service hubs).

Out of scope (prototype):
- Personal account actions (fees account, grades lookup, login-based actions).
- Legal or medical advice beyond official links.
- Real-time policy updates unless present in provided source content.

### 4) Users
- Prospective students.
- Current undergraduate/postgraduate students.
- Parents/guardians (basic enquiry mode).

### 5) Functional Requirements
- Accept natural-language student questions.
- Retrieve relevant information from approved university sources.
- Return concise, helpful answers in a friendly support tone.
- Include source references in each answer.
- If confidence is low or source is missing:
  - Respond with uncertainty clearly.
  - Offer a next best step and official contact/escalation link.

### 6) Non-Functional Requirements
- Accuracy first over creativity.
- Safety: no fabricated policies, dates, or contacts.
- Transparency: responses should be source-backed.
- Usability: response in under 5 seconds for typical queries (prototype target).

### 7) Solution Approach (High Level)
Use a retrieval-augmented generation (RAG) pipeline:
1. Curate university information pages/documents.
2. Chunk and index content in a vector store.
3. Retrieve top relevant chunks per question.
4. Generate answer using retrieved context only.
5. Return answer with citations and fallback/escalation when uncertain.

### 8) Response and Safety Policy
- Only answer from trusted indexed content.
- Never invent deadlines, email addresses, or policy details.
- For wellbeing/crisis-related prompts, prioritize official support contacts and emergency guidance from approved sources.
- For ambiguous prompts, ask one clarifying question.

### 9) Evaluation Plan
Prepare a test set of 20-30 realistic student questions across all required categories.

Target metric:
- At least 80% acceptable answers (correct, relevant, and source-backed).

Track:
- Answer correctness.
- Citation relevance.
- Hallucination rate (target: near zero).
- Fallback quality for unknown questions.

### 10) Demo Plan
Demo script (6-8 queries):
- 1 admissions question.
- 1 assessment policy question.
- 1 deadline question.
- 1 wellbeing support question.
- 1 general enquiry.
- 1 ambiguous query requiring clarification.
- 1 out-of-scope query showing safe fallback/escalation.

### 11) Risks and Mitigation
- Outdated content: timestamp data sources and keep source list visible.
- Hallucinations: strict prompt constraints and retrieval-only grounding.
- Missing coverage: clear fallback message and contact routing.
