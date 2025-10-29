FROM python:3.12.3-slim

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
ENV UV_COMPILE_BYTECODE=1

# Use the frontend project definition
COPY frontend/pyproject.toml ./pyproject.toml

# Copy the frontend application code under /app/src
COPY frontend/src/ ./src

# Install dependencies from the frontend project
RUN pip install --no-cache-dir uv \
	&& uv pip install --system .

# Ensure Python prefers live source during development/hot-reload
ENV PYTHONPATH=/app/src:${PYTHONPATH}

# Frontend-specific config and optional assets
COPY frontend/.streamlit ./.streamlit
COPY frontend/.variables ./.variables
# Optional shared media directory
COPY media ./media

# Expose Streamlit port
EXPOSE 8501

CMD ["streamlit", "run", "src/streamlit-app.py"]
