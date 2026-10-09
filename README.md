# Enterprise Agentic RAG Assistant

A production-style Agentic RAG system for enterprise document intelligence. It combines a FastAPI backend, LangGraph agent workflow, Qdrant vector search, NeMo Guardrails, LLM-based reranking, Langfuse tracing, Logfire monitoring, Streamlit UI, and an evaluation pipeline.

This project is designed as an interview-ready backend + AI systems showcase: it demonstrates how a real RAG application can separate UI, API, retrieval, guardrails, observability, ingestion, and evaluation into clean modules.


---

## What This Project Does

The assistant answers questions from a curated technical documentation corpus while filtering unsafe/off-topic input, retrieving relevant chunks, reranking context, generating grounded answers, and tracing the full request path.

Core flow:

```text
User -> Streamlit UI -> FastAPI /query -> Guardrails -> LangGraph Agent
     -> Planner -> Retriever -> Qdrant -> Reranker -> Responder -> LLM
     -> Final Answer + Sources + Trace
```

---

## Key Features

- **Agentic RAG workflow**: LangGraph planner, retriever, and responder nodes.
- **Guardrails before retrieval**: NeMo Guardrails checks the user request before expensive search/LLM calls.
- **Vector search**: Qdrant Cloud stores indexed document chunks and serves semantic retrieval.
- **LLM-based reranking**: retrieved chunks are reranked before answer generation.
- **Session memory**: LangGraph `MemorySaver` keeps conversation context by `thread_id`.
- **Central LLM gateway layer**: all main generation calls go through `app/gateway`.
- **Observability**: Langfuse traces request-level spans and LLM calls; Logfire captures backend events.
- **Document ingestion**: local parsers handle PDF, HTML, TXT, DOCX, and PPTX files.
- **Evaluation suite**: RAGAS/custom evaluation pipeline for checking answer quality.
- **Deployment-ready backend**: Dockerfile for container platforms.

---

## Architecture

```mermaid
graph TD
    User((User)) --> UI[Streamlit UI]
    UI --> API[FastAPI Backend]
    API --> Guard{NeMo Guardrails}
    Guard -->|Blocked| Blocked[Safe Response]
    Guard -->|Allowed| Agent[LangGraph Agent]
    Agent --> Planner[Planner Node]
    Planner -->|Conversational| Responder[Responder Node]
    Planner -->|Technical Query| Retriever[Retriever Node]
    Retriever --> Qdrant[(Qdrant Vector DB)]
    Qdrant --> Reranker[LLM Reranker]
    Reranker --> Responder
    Responder --> Gateway[LLM Gateway Layer]
    Gateway --> LLM[OpenAI-Compatible LLM]
    LLM --> API
    API --> UI
    Agent -.-> Memory[(Session Memory)]
    API -.-> Langfuse[Langfuse Tracing]
    API -.-> Logfire[Logfire Monitoring]
```

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend API | FastAPI, Uvicorn |
| Agent orchestration | LangGraph, LangChain |
| LLM interface | OpenAI-compatible API, LangChain OpenAI |
| Vector database | Qdrant Cloud |
| Guardrails | NeMo Guardrails |
| Reranking | LLM-based reranker |
| Observability | Langfuse, Pydantic Logfire |
| UI | Streamlit |
| Evaluation | RAGAS-style evaluation pipeline, custom metrics |
| Deployment | Docker|

---

## Project Structure

```text
.
+-- app/
|   +-- agents/
|   |   +-- graph.py
|   |   +-- state.py
|   |   +-- nodes/
|   |       +-- planner.py
|   |       +-- retriever.py
|   |       +-- responder.py
|   +-- gateway/
|   |   +-- client.py
|   +-- guardrails/
|   |   +-- rails.py
|   |   +-- colang_rules.py
|   +-- ingestion/
|   |   +-- processor.py
|   |   +-- chunking/
|   |   +-- loaders/
|   +-- services/
|   |   +-- retrieval/
|   +-- config.py
|   +-- main.py
+-- ui/
|   +-- app.py
+-- evals/
+-- DOCS/
+-- DATA/
+-- Dockerfile
+-- requirements.txt
+-- requirements-prod.txt
```

---






## Documentation

| Guide | Description |
| --- | --- |
| [System Overview](DOCS/01_SYSTEM_OVERVIEW.md) | End-to-end system flow |
| [Ingestion Engine](DOCS/02_INGESTION_ENGINE.md) | Document parsing and chunk indexing |
| [Node Intelligence](DOCS/03_NODE_INTELLIGENCE.md) | Planner, retriever, responder internals |
| [Tracing and Observability](DOCS/04_TRACING_AND_OBSERVABILITY.md) | Logfire and tracing design |
| [Environment Variables](DOCS/05_ENVIRONMENT_VARIABLES.md) | Configuration reference |
| [Known Gotchas](DOCS/06_KNOWN_GOTCHAS.md) | Bugs, fixes, and design notes |
| [Reranking](DOCS/07_FLASHRANK_RERANKING.md) | Reranking strategy |
| [Guardrails](DOCS/08_GUARDRAILS.md) | NeMo Guardrails implementation |
| [LLM Gateway](DOCS/09_LLM_GATEWAY.md) | Gateway abstraction and routing |
| [Evals](DOCS/10_EVALS.md) | Evaluation theory and metrics |
| [Evals Pipeline](DOCS/11_EVALS_PIPELINE.md) | Live evaluation workflow |

---

## Interview Summary

This project demonstrates how to build an enterprise-style RAG system with clean separation between UI, API, agent orchestration, retrieval, guardrails, observability, and evaluation.

It is demo-ready and deployment-ready for portfolio/interview use. For a public production rollout, the next hardening steps would be authentication, rate limiting, CI tests, stricter dependency pinning, and deployment monitoring.
