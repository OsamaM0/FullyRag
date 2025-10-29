<p align="center">
  <img src="media/polyrag.svg" alt="PolyRAG Logo" width="200"/>
</p>

**PolyRAG is a modular agentic RAG framework optimized for SLM (small language models) with small context windows**

➡️ Full project documentation is now centralized in `docs/`. Start here: docs/index.md

<img src="media/schema-data.png" alt="PolyRAG Architecture" width="800"/>

*Agents and tools are designed to pipe outputs directly, auto-correct imperfect inputs, and minimize main agent context load. Every feature is built for small, slow, or local LLMs.*

---

> **Modular: Bring Your Own Data, Lexicon, and LLM**
>
> This repo uses MedRxiv publications as a demo, but you can connect PolyRAG to any database, lexicon, or document set—just adapt the system prompt and DB connection. Any LLM backend is supported. Indexing scripts are in [`scripts/`](scripts/). See "Customization" below.

---

## Agentic Architecture


<img src="media/demo_3.png" alt="PolyRAG Smart Actions" width="800"/>

*Suggestion of actions at the creation of a new conversation*

---

### Conversational Research Assistant
<img src="media/demo_1.png" alt="PolyRAG Chat Interface" width="800"/>

*Ask complex research questions and get precise, sourced answers. Accesses lexicon, finds paragraphs in documents*

---

### Contextual PDF Highlighting
<img src="media/demo_4.png" alt="PolyRAG PDF Highlighting" width="800"/>

*View PDFs with automatically highlighted, contextually relevant blocks—extracted.*

---

### Data Visualization from Natural Language (Agent-Tool Chaining)
<img src="media/demo_2.png" alt="PolyRAG Data Visualization" width="800"/>

*Generate publication trend graphs and other visualizations from natural language requests, with results piped through the agent-tool chain.*

---

### End-to-End Agent Orchestration
<img src="media/example.png" alt="PolyRAG Agent Orchestration" width="800"/>

*See how PolyRAG chains SQL, RAG, and PDF tools to answer technical questions—each step*

---

## Document Extraction & Indexing

- **Semi-structured Extraction:**
  - Uses NLM Ingestor and Tika with data type detection and tree structure.
  - Localization and regex rules for extracting structured parts.
  - Produces a structure with type, parent, child, and position.

- **Indexing:**
  - Uses PostgreSQL TSVector (French) for efficient, scalable full-text search with tokenization and stemming.
  - No embeddings by default: lighter, scalable, and future-ready for on-premise models.
  - Excellent performance for technical queries.

---

## Features Overview

- Agentic RAG: Modular agents for database and document queries.
- Interactive PDF viewer with contextual highlights.
- Natural language to SQL and graphing, coordinated by agents.
- Conversation history, feedback, and moderation.
- Docker and Python support for easy deployment.


## ⚡ Quick Start

### Run with Python

```sh
# Set required environment variables. Check in .env.example for values to put in .env

# Install dependencies (uv recommended)
pip install uv
uv sync --frozen
source .venv/bin/activate

# Run the service
python src/run_service.py

# In another terminal
source .venv/bin/activate
streamlit run src/streamlit-app.py
```

---

### Run with Docker

```bash
# From the repo root
docker compose -f compose.yaml up --build
```

Services:
- Backend API at http://localhost:8080
- Streamlit app at http://localhost:8501
- PostgreSQL at localhost:5433 (container port 5432)

To stop:
```bash
docker compose -f compose.yaml down
```

---

## 🗄️ Database Setup

To quickly get started with real data as shown in the screenshots, you can populate your PostgreSQL database using the following dump:

**[Download the demo database dump (Google Drive)](https://drive.google.com/file/d/1sN6-1vx18vGjRGosKPJtoLiocb_ulP56/view?usp=sharing)**

This dump contains metadata and vectorized PDFs from medrxiv (first half of 2025), enabling you to reproduce the demo experience out of the box.

To restore the dump:
```sh
# Example command (adjust connection details as needed)
pg_restore -d your_database_name -U your_postgres_user -h your_postgres_host -p your_postgres_port /path/to/downloaded/dump_file
```

---

## ⚙️ Configuration

All configuration is handled via environment variables in your `.env` file. See `.env.example` for a full list. Key options include:

- `OPENAI_API_KEY`, `AZURE_OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `GROQ_API_KEY`: API keys for supported LLM providers.
- `USE_AWS_BEDROCK`: Enable Amazon Bedrock integration (`true`/`false`).
- `AWS_KB_ID`: Amazon Bedrock Knowledge Base ID.
- `DATABASE_URL`: PostgreSQL connection string.
- `SCHEMA_APP_DATA`: Database schema for application data (default: `document_data`).
- `LANGUAGE`: **Default UI language** (options: `english`, `arabic`, `en`, `ar`). See [Language Configuration Guide](docs/language.md) for details.
- `NLM_INGESTOR_API`: URL for the NLM Ingestor service.
- `UPLOADED_PDF_PARSER`: Parser for uploaded PDFs (`pypdf`, `nlm-ingestor`, etc.).
- `DISPLAY_TEXTS_JSON_PATH`: Path to display texts JSON.
- `SYSTEM_PROMPT_PATH`: Path to the system prompt file.
- `NO_AUTH`: Set to `True` to disable authentication (not recommended for production).

Copy `.env.example` to `.env` and fill in the required values for your setup.

### 🌍 Language Configuration

PolyRAG supports multiple languages with full RTL support. To configure the default language:

**Quick Setup:**
```bash
# Linux/Mac
./scripts/configure_language.sh

# Windows PowerShell
.\scripts\configure_language.ps1
```

**Manual Setup:**
Edit `.env` file:
```env
LANGUAGE=english  # Options: english, arabic, en, ar
```

**Supported Languages:**
- English (default)
- Arabic (with RTL support)

📖 **Full Documentation:** See [Language Configuration Guide](docs/language.md) for complete details.

---

## 🛠️ Customization: Connect Your Own Data, Lexicon, and LLM

PolyRAG is designed to be easily adapted to your own use case—across any domain, database, or document set. The MedRxiv setup provided here is just a showcase.

**To use PolyRAG with your own data:**

1. **Database Connection:**
   - Edit the `DATABASE_URL` in your `.env` file to point to your own PostgreSQL (or compatible) database.
   - Adjust schema/table names as needed in your configuration.

2. **System Prompt:**
   - Adapt the system prompt file (see the `SYSTEM_PROMPT_PATH` variable in your `.env`) to fit your domain, lexicon, and user instructions.

3. **Indexing Your Data:**
   - Use the scripts in the [`scripts/`](scripts/) directory to index your own documents:
     - `index-folder-script.py`: Index documents from a local folder.
     - `index-urls-script.py`: Index documents from a list of URLs.
     - `scrape_arxiv.py`, `scrape_medrxiv.py`: Example scrapers for scientific sources.
   - You can create your own scripts following these templates for other data sources.

4. **LLM Backend:**
   - PolyRAG is backend-agnostic. Set the appropriate API key(s) in your `.env` to use OpenAI, Mistral, DeepSeek, Anthropic, Google, Groq, or your own local LLM.

5. **Display Texts & Instructions:**
   - Customize user-facing texts and instructions by editing the files referenced in your `.env` (e.g., `DISPLAY_TEXTS_JSON_PATH`, `instructions.md`).

**For more advanced customization, see the code in the `src/` directory and adapt agents, tools, or workflows as needed.**
