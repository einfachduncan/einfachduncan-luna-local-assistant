import json
import requests
from typing import List, Dict, Generator

from config import (
    LLM_BACKEND,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    LMSTUDIO_BASE_URL,
    LMSTUDIO_MODEL,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
)


def chat_completion(messages: List[Dict[str, str]]) -> str:
    if LLM_BACKEND == "ollama":
        return ollama_chat(messages)
    if LLM_BACKEND == "lmstudio":
        return lmstudio_chat(messages)
    raise ValueError(f"Unsupported backend: {LLM_BACKEND}")


def stream_chat_completion(messages: List[Dict[str, str]]) -> Generator[str, None, None]:
    if LLM_BACKEND == "ollama":
        yield from ollama_chat_stream(messages)
        return
    text = chat_completion(messages)
    yield text


def ollama_chat(messages: List[Dict[str, str]]) -> str:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "num_predict": MAX_TOKENS,
        }
    }
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]


def ollama_chat_stream(messages: List[Dict[str, str]]) -> Generator[str, None, None]:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "num_predict": MAX_TOKENS,
        }
    }

    with requests.post(url, json=payload, timeout=300, stream=True) as r:
        r.raise_for_status()
        accumulated = ""
        for line in r.iter_lines():
            if not line:
                continue
            data = json.loads(line.decode("utf-8"))
            chunk = data.get("message", {}).get("content", "")
            if chunk:
                accumulated += chunk
                yield accumulated


def lmstudio_chat(messages: List[Dict[str, str]]) -> str:
    url = f"{LMSTUDIO_BASE_URL}/chat/completions"
    payload = {
        "model": LMSTUDIO_MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "stream": False,
    }
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]
