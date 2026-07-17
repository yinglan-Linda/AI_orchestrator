import requests
import json

# Ollama's default local server endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"

def query_qwen(prompt, model="qwen2.5:0.5b"):
    """Send a prompt to the local Ollama service and get the model's response"""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,  # one answer for one question
        "options": {
            "num_predict": 512  # limit response, reduce cost
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()  # check status
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"调用本地模型时出错: {e}"