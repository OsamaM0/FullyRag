# Troubleshooting and Quick Fixes

Consolidated from the previous quick‑fix notes.

## Common fixes after separation

1) ModuleNotFoundError (frontend importing backend)
- Remove backend imports from frontend modules
- Use `AgentClient` for HTTP calls

2) Missing configuration directories
- Ensure `.streamlit/` and `.variables/` exist in `frontend/`

## Running

Frontend
```bash
cd frontend
source .venv/bin/activate
streamlit run src/streamlit-app.py
```

Backend
```bash
cd backend
source .venv/bin/activate
python src/run_service.py
```

Set in `frontend/.env`:
```env
AGENT_URL=http://localhost:8080
```

## Environment samples

Frontend `.env`
```env
AGENT_URL=http://localhost:8080
NO_AUTH=True
AUTH_SECRET=your-secret-key
```

Backend `.env`
```env
HOST=0.0.0.0
PORT=8080
AUTH_SECRET=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/fullyrag
OPENAI_API_KEY=...
```

## Known warnings

- psycopg_binary uninstall warning: cosmetic; can ignore or `uv sync --reinstall`
- theme.sidebar.color deprecation: remove from `.streamlit/config.toml`

## Links

- Architecture: docs/architecture.md
- Backend docs: backend/README.md
- Frontend docs: frontend/README.md
