# Architecture

This page consolidates the visual architecture, data flow, file layout, API endpoints, and deployment options for PolyRAG.

## Visual overview

```
<diagrams omitted for brevity — see data flow and components below>
```

## Components and flow

User → Streamlit (frontend) → FastAPI (backend) → PostgreSQL

High‑level data path for a question:
1) Frontend sends request to backend `/stream`
2) Backend agent manager orchestrates tools (RAG, SQL, plotting)
3) RAG searches PostgreSQL TSVector blocks
4) LLM generates answer; tokens are streamed back to frontend

## File organization (abridged)

Backend
```
backend/src/
  agents/           # Agent logic and tools
  service/          # FastAPI routes
  core/             # LLM clients, settings
  memory/           # Checkpointers (postgres, sqlite)
  schema/           # Pydantic models and API schemas
  db_manager.py     # DB operations
  rag_system.py     # RAG implementation
  security.py       # Auth & security
  run_service.py    # Entrypoint
```

Frontend
```
frontend/src/
  client/           # HTTP client
  frontend/         # UI components (chat, pdf viewer, feedback, user)
  schema/           # Shared models
  streamlit-app.py  # App entry
  display_texts.py  # i18n texts
  multilanguage_css.py
  auth_helpers.py
```

## API endpoints (core)

- GET /health
- GET /info
- POST /{agent_id}/invoke
- POST /{agent_id}/stream
- POST /history
- GET /conversations
- GET/POST /conversations/{id}/title
- DELETE /conversations/{id}
- POST /upload
- POST /feedback
- GET /feedback/{run_id}
- POST /rag/annotations
- POST /rag/debug_blocks
- GET /documents/{name}/source_status

## Network topologies

Development (single machine)
- Frontend http://localhost:8501 → Backend http://localhost:8080 → DB :5433

Production
- Frontend on app domain → Backend on API domain → managed or private DB

## Deployment patterns

- Single host (all services on one server)
- Split servers (frontend, backend, db separately)
- Cloud scaling with load balancers

## Summary

- Independent development and scaling for FE/BE
- Simple, observable HTTP communication
- PostgreSQL FT search for performant, embedding‑free retrieval by default
