"""
LangChain service module for DCI AI Business Assistant using ChatOllama and prompt template chain.
"""

from langchain_core.output_parsers import StrOutputParser
# pyrefly: ignore [missing-import]
from langchain_ollama import ChatOllama

from backend.config import OLLAMA_MODEL
from prompts.langchain_prompts import BUSINESS_CHAT_PROMPT

# Create ChatOllama model instance
model = ChatOllama(model=OLLAMA_MODEL)

# Create StrOutputParser instance
parser = StrOutputParser()

# Combine prompt template, model, and output parser into a chain
chain = BUSINESS_CHAT_PROMPT | model | parser


async def generate_langchain_response(message: str) -> str:
    """
    Send a message through the LangChain prompt chain asynchronously and return plain text response.
    """
    response = await chain.ainvoke({"message": message})
    return response


