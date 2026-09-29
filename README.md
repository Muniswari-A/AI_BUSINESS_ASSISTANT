# DCI AI Business Assistant

An enterprise-grade, agentic AI business support platform built with **FastAPI**, **LangGraph**, **Model Context Protocol (MCP)**, **Chroma Vector DB (RAG)**, **SQLite**, and **Ollama**.

---

## Project Overview

The **DCI AI Business Assistant** processes customer requests through an intelligent multi-node workflow. It performs customer and complaint lookup via SQLite database tools running over MCP, retrieves company policies using a vector RAG pipeline, and executes ticket creation actions.

---

## Features

- **Agentic Workflow Architecture**: Multi-stage state graph built using `LangGraph`.
- **Model Context Protocol (MCP)**: Decoupled tool server (`mcp_server/server.py`) managing database queries via standard input/output interface.
- **SQLite Database Persistence**: Stores customers, complaints, and ticket data permanently in `mcp_server/business.db`. Sequential ticket IDs (`T001`, `T002`, ...) persist seamlessly across server restarts.
- **Retrieval-Augmented Generation (RAG)**: Policy search using `Chroma` and HuggingFace embeddings (`all-MiniLM-L6-v2`).
- **Interactive Web Interface**: Clean frontend served directly via FastAPI at `/`.
- **Ollama LLM Integration**: Uses local LLM inference (`llama3.2`).

---

## Architecture

```
User Request
    │
    ▼
FastAPI App (/api/assistant)
    │
    ▼
LangGraph Workflow
    ├── Understand Request Node (Intent & Customer extraction)
    ├── Retrieve Information Node (MCP DB queries & RAG policy search)
    ├── Business Analysis Node (Rule-based ticket decision logic)
    ├── Action Node (Executes MCP create_ticket tool)
    └── Final Response Node (Generates customer-facing message)
    │
    ▼
FastAPI Response
```

---

## Project Structure

```
DCI_AI_BUSINESS_ASSISTANT/
├── backend/
│   ├── main.py                # FastAPI gateway & endpoints
│   ├── config.py              # Application configuration & env loading
│   ├── ai_service.py          # Direct Ollama chat service
│   └── langchain_service.py   # LangChain ChatOllama chain
├── graph/
│   ├── business_graph.py      # LangGraph state graph definition & router
│   ├── nodes.py               # Workflow node implementations
│   └── state.py               # BusinessState schema definition
├── mcp_server/
│   ├── server.py              # FastMCP server (tools for DB operations)
│   ├── db.py                  # SQLite database connection & seeding
│   ├── client.py              # Stdio MCP client context manager
│   └── mcp_service.py         # Helper functions for MCP tool execution
├── rag/
│   ├── rag_service.py         # Document loading, vector database & retrieval
│   └── rag_chain.py           # Standalone RAG chat chain
├── agents/
│   ├── business_crew.py       # CrewAI multi-agent crew runner
│   ├── crew_agents.py         # CrewAI agent definitions
│   ├── crew_tasks.py          # CrewAI task definitions
│   ├── langchain_agent.py     # Tool-bound ChatOllama agent
│   ├── customer_tools.py      # Customer tool definition
│   └── tools.py               # Standalone customer lookup tool
├── documents/
│   ├── customer_support_policy.txt
│   └── refund_policy.txt
├── frontend/
│   └── index.html             # Web UI interface
├── prompts/                   # System & few-shot prompts
├── tests/                     # Comprehensive Pytest test suite
├── .env                       # Environment variables
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Project dependencies
└── README.md                  # Comprehensive project documentation
```

---

## Requirements

- **Python**: `3.10` or higher
- **Ollama**: Installed and running locally (`ollama serve`)
- **Model**: `llama3.2` pulled (`ollama pull llama3.2`)

---

## Installation & Setup

### 1. Clone & Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create or verify `.env` in the project root:

```env
APP_NAME=DCI AI Business Assistant
APP_VERSION=1.0.0
OLLAMA_MODEL=llama3.2
```

### 4. Ollama Setup

Ensure Ollama is running and download the model:

```bash
ollama pull llama3.2
```

---

## Running the Application

Start the FastAPI backend with Uvicorn:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Access points:
- **Web UI**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## Running Tests

Execute the full automated test suite:

```bash
python -m pytest tests/ -v -s
```

Run specific test modules:

```bash
# Test database persistence & sequential ticket ID generation:
python -m pytest tests/test_database_persistence.py -v -s

# Test agentic workflow scenarios:
python -m pytest tests/test_agentic_workflow.py -v -s
```

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves web application UI |
| `GET` | `/health` | Health check (app status & Ollama reachability) |
| `POST` | `/api/assistant` | Main endpoint for business requests & agentic workflow |
| `POST` | `/chat` | Direct conversation endpoint |
| `POST` | `/agent` | LangChain customer lookup agent endpoint |

### Example Request (`POST /api/assistant`)

```json
{
  "message": "Ravi Kumar has a damaged product. Create a ticket."
}
```

### Example Response

```json
{
  "message": "Ravi Kumar has a damaged product. Create a ticket.",
  "response": "Dear Ravi Kumar, ticket T001 has been opened for your damaged product issue.",
  "decision": "CREATE_TICKET",
  "ticket": "Ticket T001 created successfully. Status: Open"
}
```

---

## Troubleshooting & Known Warnings

1. **Browser access to `0.0.0.0`**: On Windows, navigate to `http://localhost:8000` or `http://127.0.0.1:8000` (browsers on Windows do not resolve `0.0.0.0` directly).
2. **Pytest Asyncio Configuration**: `pytest.ini` specifies `asyncio_mode = auto` for seamless async test execution.
3. **Chroma Vector DB Rebuilding**: If vector DB files are moved or corrupted, `rag/rag_service.py` automatically detects and rebuilds the database safely.

---

## Production Deployment

For production deployments, the following architectural adjustments are recommended:

### Local Development Requirements
- **LLM**: Local Ollama instance (`llama3.2` model).
- **Database**: SQLite (`mcp_server/business.db`) for lightweight local persistence.
- **Server**: Uvicorn running on a single worker (`uvicorn backend.main:app`).

### Production Deployment Requirements
- **LLM**: Use a managed/cloud LLM endpoint or a dedicated high-memory GPU instance for Ollama.
- **Database**: Migrate from SQLite to PostgreSQL (update connection strings in `mcp_server/db.py`).
- **Server**: Run Uvicorn behind Gunicorn or Nginx with multiple workers for concurrency:
  ```bash
  gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
  ```
- **Environment**: Secure `.env` variables (`OLLAMA_MODEL`, database credentials).
