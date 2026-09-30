# Configuration settings for DCI AI Business Assistant backend
import os

from dotenv import load_dotenv

load_dotenv()


APP_NAME = os.getenv(
    "APP_NAME",
    "DCI AI Business Assistant"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)
