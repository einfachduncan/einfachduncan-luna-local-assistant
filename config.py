import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "Luna")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "7860"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")  # ollama | lmstudio

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "local-model")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.9"))
TOP_P = float(os.getenv("TOP_P", "0.95"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

ENABLE_MEMORY = os.getenv("ENABLE_MEMORY", "true").lower() == "true"
SQLITE_PATH = os.getenv("SQLITE_PATH", "data/memories.db")
MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", "12"))
MAX_CONTEXT_MEMORIES = int(os.getenv("MAX_CONTEXT_MEMORIES", "6"))

ENABLE_WEB_SEARCH = os.getenv("ENABLE_WEB_SEARCH", "true").lower() == "true"
ENABLE_FILE_TOOLS = os.getenv("ENABLE_FILE_TOOLS", "true").lower() == "true"
ENABLE_VOICE = os.getenv("ENABLE_VOICE", "false").lower() == "true"

DATA_DIR = os.getenv("DATA_DIR", "data")
FILES_DIR = os.getenv("FILES_DIR", "data/files")
EXPORT_DIR = os.getenv("EXPORT_DIR", "data/chat_exports")
PERSONA_FILE = os.getenv("PERSONA_FILE", "prompts/persona.txt")
CUSTOM_CSS = os.getenv("CUSTOM_CSS", "static/luna.css")
