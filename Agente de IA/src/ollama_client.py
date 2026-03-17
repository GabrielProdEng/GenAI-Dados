from __future__ import annotations

from typing import Any

import requests

OLLAMA_BASE_URL = "http://localhost:11434"
TIMEOUT = 120


def list_models() -> list[str]:
    """
    Lista modelos disponíveis localmente no Ollama.
    """
    url = f"{OLLAMA_BASE_URL}/api/tags"
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    data = response.json()
    models = data.get("models", [])
    return [model["name"] for model in models if "name" in model]


def chat(
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.2,
) -> str:
    """
    Envia uma conversa para o endpoint /api/chat do Ollama.
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    response = requests.post(url, json=payload, timeout=TIMEOUT)
    response.raise_for_status()

    data = response.json()
    message = data.get("message", {})
    return message.get("content", "").strip()
