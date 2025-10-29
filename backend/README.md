# PolyRAG Backend Service

**Backend service for PolyRAG - AI agent service built with LangGraph and FastAPI**

This is the backend/API service that powers the PolyRAG agentic RAG system. It provides REST API endpoints for AI agent interactions, document processing, RAG operations, and conversation management.

## 🚀 Features

- **LangGraph-Powered Agents**: Modular agentic architecture with custom tools
- **FastAPI REST API**: High-performance async API endpoints
- **RAG System**: Document indexing and retrieval with PostgreSQL full-text search
- **Database Management**: PostgreSQL with LangGraph checkpointing for conversation state
- **Multi-LLM Support**: OpenAI, Anthropic, Google, DeepSeek, Groq, and more
- **Authentication**: Secure API endpoints with bearer token authentication
- **File Upload**: PDF and text file processing with multiple parsers
- **Feedback System**: Track user feedback and conversation analytics

## 📋 Prerequisites

- Python 3.12 or higher
- PostgreSQL 15 or higher
- (Optional) Docker and Docker Compose

## 🔧 Installation

### Option 1: Local Development with Python

1. **Clone and navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   pip install uv
   uv sync --frozen
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up PostgreSQL database**
   - Create a database named `polyrag`
   - Update `DATABASE_URL` in `.env` with your connection string

5. **Run the service**
   ```bash
   python src/run_service.py
   ```

   The API will be available at `http://localhost:8080`

### Option 2: Docker (recommended for full stack)

1. **Configure environment (repo root)**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start the stack from repo root**
   ```bash
   docker compose -f compose.yaml up --build -d
   ```

   This will start:
   - Backend API service on port 8080
   - Streamlit app on port 8501
   - PostgreSQL database on port 5433

3. **View logs**
   ```bash
   docker compose -f compose.yaml logs -f agent-service
   ```

## 🌐 API Endpoints

Once running, visit `http://localhost:8080/docs` for the interactive API documentation (Swagger UI).

### Key Endpoints

- **POST** `/invoke` - Invoke an agent with a message
- **POST** `/stream` - Stream agent responses with tokens
- **POST** `/history` - Get conversation history
- **POST** `/feedback` - Submit feedback for a conversation
- **POST** `/upload` - Upload files (PDF, text)
- **GET** `/conversations` - List user conversations
- **GET** `/info` - Get service metadata and available models

## ⚙️ Configuration

Key environment variables (see `.env.example` for full list):

### Server Configuration
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8080`)
- `AUTH_SECRET`: Secret key for API authentication

### LLM Configuration
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GOOGLE_API_KEY`: Google AI API key
- `DEEPSEEK_API_KEY`: DeepSeek API key

### Database Configuration
- `DATABASE_URL`: PostgreSQL connection string
- `SCHEMA_APP_DATA`: Database schema name (default: `document_data`)

### Document Processing
- `NLM_INGESTOR_API`: NLM Ingestor service URL for PDF parsing
- `UPLOADED_PDF_PARSER`: PDF parser to use (`pypdf` or `nlm-ingestor`)

## 🔍 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src
```

## 📁 Project Structure

```
backend/
├── src/
│   ├── agents/           # LangGraph agent definitions
│   ├── service/          # FastAPI service and routes
│   ├── core/             # Core settings and LLM configuration
│   ├── memory/           # Database checkpointer implementations
│   ├── schema/           # Pydantic models and schemas
│   ├── db_manager.py     # Database operations
│   ├── rag_system.py     # RAG indexing and retrieval
│   ├── security.py       # Authentication utilities
│   └── run_service.py    # Service entry point
├── scripts/              # Data indexing scripts
├── (built via repo-root docker/Dockerfile.service and compose.yaml)
├── pyproject.toml        # Python dependencies
└── README.md            # This file
```

## 🔌 Client Integration

This backend is designed to work with the PolyRAG frontend application. You can also integrate it with custom clients using the HTTP REST API.

Example using `httpx`:

```python
import httpx

response = httpx.post(
    "http://localhost:8080/invoke",
    json={
        "message": "What are the latest trends in AI research?",
        "thread_id": "user-123-conv-456"
    },
    headers={"Authorization": "Bearer your-secret-key"}
)

print(response.json())
```

## 🛠️ Development

### Hot Reload

The service supports hot reload during development:

```bash
python src/run_service.py
```

Changes to Python files will automatically restart the service.

### Database Migrations

When modifying database schemas:

1. Update models in `src/schema/`
2. Run migrations (if using Alembic)
3. Update `db_manager.py` as needed

## 📊 Monitoring

- Health check endpoint: `GET /health`
- Metrics and logs available through Docker logs or application logs

## 🐛 Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check `DATABASE_URL` in `.env`
- Ensure database exists and is accessible

### LLM API Errors
- Verify API keys are correct in `.env`
- Check API rate limits and quotas
- Review service logs for specific error messages

### Port Already in Use
- Change `PORT` in `.env` to an available port
- Or stop the service using the port: `lsof -ti:8080 | xargs kill`

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues and questions, please open a GitHub issue or contact the maintainers.
