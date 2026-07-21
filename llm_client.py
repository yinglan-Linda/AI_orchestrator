import requests
import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
# load environment variables from .env file first
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

MODEL_ROUTING = {
    "coding":  {"model": "openrouter/free", "max_tokens": 1024},
    "academic": {"model": "openrouter/free", "max_tokens": 2048},
    "humanize": {"model": "openrouter/free", "max_tokens": 512},
    "general": {"model": "openrouter/free", "max_tokens": 768},
}

def calculate_dynamic_max_tokens(prompt, base_max_tokens):
    input_length = len(prompt.split())
    if input_length < 20:
        return min(base_max_tokens, 256)
    elif input_length < 100:
        return base_max_tokens
    else:
        return min(base_max_tokens * 2, 4096)

def fallback_to_ollama(prompt):
    """Fallback to local Ollama model if OpenRouter fails."""
    local_model = "qwen2.5:0.5b"
    payload = {
        "model": local_model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 512}
    }
    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=60)
        if response.status_code == 200:
            content = response.json()["response"]
            return {"content": content, "model": local_model, "source": "ollama"}
        else:
            return {"content": "Local model call failed", "model": local_model, "source": "error"}
    except Exception as e:
        return {"content": f"Fallback call failed: {e}", "model": "none", "source": "error"}

def query_router(prompt, agent_type="general", retries=2):
    """Call OpenRouter, retry on failure, fallback to local Ollama if all fail"""
    model_config = MODEL_ROUTING.get(agent_type, MODEL_ROUTING["general"])
    model = model_config["model"]
    max_tokens = calculate_dynamic_max_tokens(prompt, model_config["max_tokens"])

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }

    for attempt in range(retries):
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                content = response.json()["choices"][0]["message"]["content"]
                return {"content": content, "model": model, "source": "openrouter"}
            else:
                # Status code is not 200, consider it a failure and continue retrying
                print(f"OpenRouter returned status code {response.status_code}, retrying {attempt+1}/{retries}")
        except Exception as e:
            print(f"OpenRouter call exception: {e}, retrying {attempt+1}/{retries}")

        if attempt < retries - 1:
            time.sleep(1)  # Wait 1 second before retrying

    # All retries failed, fallback to local
    print("All OpenRouter retries failed, falling back to local Ollama")
    return fallback_to_ollama(prompt)
