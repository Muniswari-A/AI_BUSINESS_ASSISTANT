import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import ollama

from backend.config import APP_NAME, APP_VERSION, OLLAMA_BASE_URL
from backend.ai_service import generate_response
from agents.langchain_agent import run_customer_agent
from graph.business_graph import business_graph
from fastapi.middleware.cors import CORSMiddleware

ollama_client = ollama.Client(host=OLLAMA_BASE_URL)

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Main API gateway for the Agentic AI Business Assistant."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    context: str = ""


class AssistantRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000, description="The natural-language business request")


class AssistantResponse(BaseModel):
    message: str
    response: str
    decision: str = ""
    ticket: str = ""


@app.get("/")
async def root():

    html_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return {
        "message": "DCI AI Business Assistant is running"
    }


@app.get("/health")
async def health():
    ollama_status = "unavailable"
    try:
        ollama_client.list()
        ollama_status = "available"
    except Exception:
        pass

    return {
        "status": "healthy",
        "ollama": ollama_status
    }


@app.post("/api/assistant", response_model=AssistantResponse)
async def assistant_endpoint(request: AssistantRequest):
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    try:
        # Check if Ollama is at least reachable before starting a long workflow
        ollama_client.list()
    except Exception:
        raise HTTPException(status_code=503, detail="Ollama service is currently unavailable.")

    try:
        result = await business_graph.ainvoke(
            {"question": request.message}
        )
        return AssistantResponse(
            message=request.message,
            response=result.get("response", ""),
            decision=result.get("decision", ""),
            ticket=result.get("ticket_result", "")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred during the workflow execution."
        )


@app.post("/chat")
async def chat(request: ChatRequest):

    response = await generate_response(
        message=request.message,
        context=request.context
    )

    return {
        "message": request.message,
        "response": response
    }


@app.post("/agent")
async def agent_chat(request: ChatRequest):

    response = await run_customer_agent(
        request.message
    )

    return {
        "message": request.message,
        "response": response
    }
