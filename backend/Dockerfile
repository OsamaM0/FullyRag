FROM python:3.12.3-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq5 --no-install-recommends && rm -rf /var/lib/apt/lists/*

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

EXPOSE 8080

CMD ["python", "src/run_service.py"]
