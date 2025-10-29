FROM python:3.12.3-slim

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV UV_COMPILE_BYTECODE=1

# Install dependencies without requiring a uv.lock file
COPY pyproject.toml ./
COPY src/ ./src
RUN pip install --no-cache-dir uv \
	&& uv pip install --system .

# Prefer live source during development/hot-reload
ENV PYTHONPATH=/app/src:${PYTHONPATH}

COPY media ./media

EXPOSE 8501

CMD ["streamlit", "run", "src/streamlit-app.py", "--server.address", "0.0.0.0"]
