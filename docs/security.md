# Security

This page documents authentication, tokens, CORS, headers, and recommended practices.

## Authentication

- JWT access and refresh tokens
- Access: short‑lived; Refresh: longer‑lived; use `/auth/refresh`
- Store tokens server‑side in Streamlit session state (current implementation)

## Passwords

- Hash with bcrypt (salted), never store plaintext
- Enforce length and complexity requirements

## CORS

Allow only expected origins in development and production.

## API secret (service‑to‑service)

Use `AUTH_SECRET` via Authorization: Bearer for trusted internal calls.

## Best practices

- HTTPS in production (reverse proxy)
- Rotate secrets regularly
- Strong, long secrets
- Avoid logging sensitive data
- Add rate limiting and secure headers

See source for examples in backend security utilities.
