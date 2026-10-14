<div align="center">

<h1>🤖 DCI AI Business Assistant</h1>

<p>
  <strong>An enterprise-grade, agentic AI business support platform</strong><br/>
  Built with LangGraph · MCP · RAG · FastAPI · Ollama
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangGraph-Agentic-purple?style=for-the-badge&logo=langchain&logoColor=white"/>
  <img src="https://img.shields.io/badge/Ollama-llama3.2-black?style=for-the-badge&logo=ollama&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p>
  <img src="https://img.shields.io/badge/ChromaDB-RAG%20Pipeline-orange?style=flat-square"/>
  <img src="https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blueviolet?style=flat-square"/>
  <img src="https://img.shields.io/badge/CrewAI-Multi--Agent-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/SQLite-Persistent%20DB-lightblue?style=flat-square"/>
  <img src="https://img.shields.io/badge/Tests-14%20Suites-brightgreen?style=flat-square"/>
</p>

</div>

---

## 📖 Overview

The **DCI AI Business Assistant** is a fully agentic, multi-node AI platform that processes natural-language business requests end-to-end. It combines cutting-edge AI technologies into a single production-ready application:

- 🔍 **Customer & complaint lookup** via a live SQLite database over MCP
- 📚 **Policy retrieval** using a RAG pipeline (ChromaDB + HuggingFace embeddings)
- 🎫 **Automated ticket creation** with sequential, persistent ticket IDs (`T001`, `T002`, …)
- 🌐 **Interactive web UI** served directly from FastAPI
- 🧠 **Local LLM inference** via Ollama — no external API keys needed

---

## ✨ Key Features

| Feature | Technology |
|:--------|:-----------|
| **Agentic Workflow** | LangGraph StateGraph — 5-node pipeline |
| **Tool Execution** | Model Context Protocol (MCP) via stdio subprocess |
| **Policy Search** | ChromaDB + `all-MiniLM-L6-v2` HuggingFace embeddings |
| **Multi-Agent** | CrewAI crew for complex task orchestration |
| **LLM Backend** | Ollama (`llama3.2`) — fully local, offline-capable |
| **REST API** | FastAPI with Pydantic validation & auto Swagger docs |
| **Persistence** | SQLite with sequential ticket IDs that survive restarts |
| **Containerised** | Multi-stage Dockerfile with non-root user & healthcheck |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User / Web Browser                      │
└──────────────────────────┬──────────────────────────────────┘
                           │  HTTP POST /api/assistant
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Gateway                           │
│              backend/main.py  (:8000)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  LangGraph Workflow                         │
│                                                             │
│  ┌─────────────┐   ┌──────────────┐   ┌─────────────────┐  │
│  │  Understand │──▶│   Retrieve   │──▶│    Analysis     │  │
│  │  Request    │   │  Information │   │ (CREATE_TICKET?) │  │
│  └─────────────┘   └──────┬───────┘   └────────┬────────┘  │
│                           │                    │            │
│                    ┌──────┴──────┐    ┌────────▼────────┐  │
│                    │  MCP Tools  │    │  Action Node    │  │
│                    │  + RAG      │    │ (Ticket Create) │  │
│                    └─────────────┘    └────────┬────────┘  │
│                                               │            │
│                                      ┌────────▼────────┐  │
│                                      │  Final Response │  │
│                                      │  (Ollama LLM)   │  │
│                                      └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
          │                        │
          ▼                        ▼
┌──────────────────┐    ┌──────────────────────┐
│   MCP Server     │    │   ChromaDB (RAG)     │
│  mcp_server/     │    │   rag/chroma_db/     │
│  ┌────────────┐  │    │                      │
│  │  SQLite DB │  │    │  Policy Documents    │
│  │ business   │  │    │  (HuggingFace        │
│  │   .db      │  │    │   Embeddings)        │
│  └────────────┘  │    └──────────────────────┘
└──────────────────┘
```

---

## 📁 Project Structure

```
DCI_AI_BUSINESS_ASSISTANT/
│
├── 📂 backend/
│   ├── main.py                 # FastAPI app — endpoints & CORS
│   ├── config.py               # Environment variable loading
│   ├── ai_service.py           # Direct Ollama chat service
│   └── langchain_service.py    # LangChain ChatOllama chain
│
├── 📂 graph/
│   ├── business_graph.py       # LangGraph StateGraph definition
│   ├── nodes.py                # All 5 workflow node implementations
│   └── state.py                # BusinessState TypedDict schema
│
├── 📂 mcp_server/
│   ├── server.py               # FastMCP server (DB tool definitions)
│   ├── db.py                   # SQLite setup & auto-seeding
│   ├── client.py               # Stdio MCP client context manager
│   └── mcp_service.py          # call_mcp_tool() helper
│
├── 📂 rag/
│   ├── rag_service.py          # ChromaDB vector store & retriever
│   └── rag_chain.py            # Standalone RAG Q&A chain
│
├── 📂 agents/
│   ├── business_crew.py        # CrewAI crew runner
│   ├── crew_agents.py          # CrewAI agent definitions
│   ├── crew_tasks.py           # CrewAI task definitions
│   ├── langchain_agent.py      # Tool-bound ChatOllama agent
│   └── tools.py                # Custom LangChain tools
│
├── 📂 documents/               # Policy documents for RAG ingestion
├── 📂 frontend/
│   └── index.html              # React + Tailwind chat UI (served by FastAPI)
│
├── 📂 prompts/                 # System & few-shot prompt templates
├── 📂 tests/                   # 14 pytest test suites
│
├── Dockerfile                  # Multi-stage production image
├── .dockerignore
├── .env.example                # Environment variable template
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Notes |
|:------------|:------|
| Python `3.10+` | [python.org](https://www.python.org/downloads/) |
| Ollama | [ollama.com](https://ollama.com/) |
| llama3.2 model | `ollama pull llama3.2` |

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/DCI_AI_BUSINESS_ASSISTANT.git
cd DCI_AI_BUSINESS_ASSISTANT
```

### 2️⃣ Create & activate virtual environment

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment

```bash
cp .env.example .env
# Defaults work out of the box for local development
```

### 5️⃣ Start Ollama

```bash
ollama pull llama3.2
ollama serve
```

### 6️⃣ Run the application

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open your browser → **http://localhost:8000**

---

## 🐳 Docker Deployment

```bash
# Build the image
docker build -t dci-ai-assistant .

# Run (Ollama must be running on the host)
docker run -p 8000:8000 dci-ai-assistant
```

> **Note:** The container connects to Ollama at `http://host.docker.internal:11434` by default.
> Override with `-e OLLAMA_BASE_URL=<your-url>`.

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| `GET` | `/` | Serves the web chat UI |
| `GET` | `/health` | App status & Ollama reachability |
| `GET` | `/docs` | Interactive Swagger API docs |
| `POST` | `/api/assistant` | **Main** — full agentic workflow |
| `POST` | `/chat` | Direct Ollama chat (simple) |
| `POST` | `/agent` | LangChain tool-bound agent |

### Example — Create a Support Ticket

**Request:**
```bash
curl -X POST http://localhost:8000/api/assistant \
  -H "Content-Type: application/json" \
  -d '{"message": "Ravi Kumar has a damaged product. Please create a ticket."}'
```

**Response:**
```json
{
  "message": "Ravi Kumar has a damaged product. Please create a ticket.",
  "response": "Dear Ravi Kumar, I have opened ticket T001 for your damaged product issue. Our support team will contact you within 24 hours.",
  "decision": "CREATE_TICKET",
  "ticket": "Ticket T001 created successfully. Status: Open"
}
```

---

## 🧠 LangGraph Workflow — Node Details

| Step | Node | Description |
|:-----|:-----|:------------|
| 1 | **Understand Request** | Classifies intent & extracts customer name using Ollama (JSON mode) |
| 2 | **Retrieve Information** | Calls MCP tools for customer/complaint data; queries ChromaDB for policies |
| 3 | **Business Analysis** | Rule-based LLM decision: `CREATE_TICKET` / `MORE_INFORMATION_REQUIRED` / `NO_ACTION` |
| 4 | **Action** *(conditional)* | Executes `create_ticket` MCP tool; writes to SQLite with sequential IDs |
| 5 | **Final Response** | Generates a professional customer-facing response via Ollama |

---

## 🧪 Testing

```bash
# Run full test suite
python -m pytest tests/ -v -s

# Run specific modules
python -m pytest tests/test_agentic_workflow.py -v -s
python -m pytest tests/test_database_persistence.py -v -s
python -m pytest tests/test_mcp_graph.py -v -s
```

**14 test suites** covering:

- ✅ Full agentic workflow scenarios
- ✅ MCP tool execution & client
- ✅ Database persistence & sequential ticket IDs
- ✅ RAG retrieval pipeline
- ✅ FastAPI endpoint integration
- ✅ CrewAI multi-agent orchestration
- ✅ LangGraph state graph structure
- ✅ LangChain tool-bound agent

---

## ⚙️ Configuration

All settings are loaded from environment variables (see [`.env.example`](.env.example)):

| Variable | Default | Description |
|:---------|:--------|:------------|
| `APP_NAME` | `DCI AI Business Assistant` | Application display name |
| `APP_VERSION` | `1.0.0` | Application version |
| `OLLAMA_MODEL` | `llama3.2` | Ollama model to use |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |

---

## 🔧 Troubleshooting

| Issue | Fix |
|:------|:----|
| Browser can't reach `0.0.0.0` | Navigate to `http://localhost:8000` instead |
| `Ollama service unavailable` | Run `ollama serve` and ensure the model is pulled |
| ChromaDB rebuild warning | Normal on first run — vector DB is built automatically |
| Async test errors | Ensure `pytest.ini` has `asyncio_mode = auto` (already set) |

---

## 🛣️ Roadmap

- [ ] PostgreSQL migration for production scale
- [ ] Streaming responses (Server-Sent Events)
- [ ] Multi-turn conversation memory
- [ ] Authentication & multi-tenancy
- [ ] Cloud LLM fallback (OpenAI / Gemini)
- [ ] Kubernetes Helm chart

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

<div align="center">

**Built with ❤️ using LangGraph · FastAPI · MCP · ChromaDB · Ollama**

</div>
