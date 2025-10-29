# Session Management

Current behavior uses Streamlit session state for in‑session persistence. A full page refresh creates a new session.

Recommendations
- Prefer in‑app navigation over browser refresh
- If persistence across reloads is required, consider cookies (HTTP‑only), server‑side sessions, or local storage (with care)

Future improvements
- Store tokens in cookies and restore session on load

See `frontend/src/auth_storage.py` for the suggested enhancement points.
