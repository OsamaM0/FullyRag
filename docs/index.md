# FullyRAG Documentation

Welcome to the FullyRAG docs. This is the single place for setup, usage, and architecture.

- Overview
- Quick start
- Configuration
- Database (demo dump)
- Architecture
- Security
- Language and RTL support
- Session management
- Migration (monolith ➜ split)
- Troubleshooting
- Module docs (backend, frontend)

## Overview

FullyRAG is a modular, agentic RAG framework optimized for small/slow LLMs with small context windows. Agents and tools pipe outputs directly, auto-correct imperfect inputs, and minimize the main agent context load.

Key capabilities:
- Agentic RAG with modular agents/tools (SQL, RAG, PDF annotations, plotting)
- Streamlit frontend with chat, PDF viewer and highlights, feedback
- FastAPI backend with streaming and conversation history
- PostgreSQL full‑text search (TSVector) for indexing and retrieval (no embeddings by default)

## Quick start

Local quick run (Python):

```bash
# 1) Create env and install (uv recommended)
pip install uv
uv sync --frozen
source .venv/bin/activate

# 2) Start backend
python backend/src/run_service.py

# 3) In another terminal start frontend
source .venv/bin/activate
streamlit run frontend/src/streamlit-app.py
```

Docker: use the root `compose.yaml` which builds from `docker/Dockerfile.service` (backend) and `docker/Dockerfile.app` (frontend).

Quick start with Docker:

```bash
# In the repo root
docker compose -f compose.yaml up --build
```

This starts:
- agent-service (FastAPI) on port 8080
- streamlit-app on port 8501
- postgres-db on port 5433 (mapped)

## Configuration

All configuration is via `.env` files.

Important variables:
- OPENAI_API_KEY / ANTHROPIC_API_KEY / GOOGLE_API_KEY / DEEPSEEK_API_KEY / GROQ_API_KEY
- USE_AWS_BEDROCK, AWS_KB_ID (optional)
- DATABASE_URL (PostgreSQL), SCHEMA_APP_DATA (default: document_data)
- LANGUAGE (english|arabic|en|ar)
- NLM_INGESTOR_API, UPLOADED_PDF_PARSER
- DISPLAY_TEXTS_JSON_PATH, SYSTEM_PROMPT_PATH
- NO_AUTH (development only)

See details in:
- Language: docs/language.md
- Security: docs/security.md

## Database (demo dump)

To reproduce the demo quickly, restore the provided dump that contains MedRxiv metadata and vectorized PDFs:

Link: Google Drive (see project README for the latest URL)

```bash
pg_restore -d your_database -U your_user -h your_host -p your_port /path/to/dump_file
```

## Architecture

See docs/architecture.md for diagrams, data flow, API endpoints and deployment patterns.

## Security

See docs/security.md for authentication, CORS, token handling, recommended headers, and rate limiting.

## Language and RTL support

See docs/language.md for the language initialization flow, session integration, and CSS rules for RTL.

## Session management

See docs/session-management.md for current Streamlit session limitations and recommended persistence approaches.

## Migration (monolith ➜ split)

See docs/migration.md for the exact steps, configs, docker changes, and verification checklist.

## Troubleshooting

See docs/troubleshooting.md for common issues, environment samples, and quick fixes.

## Module docs

- Backend: backend/README.md
- Frontend: frontend/README.md

## Related scripts

Indexing and scraping utilities are in `scripts/` and `backend/scripts/`.
