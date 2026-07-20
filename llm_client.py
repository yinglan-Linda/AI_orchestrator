import requests
import json
import os
import time

# Ollama's default local server endpoint
# OLLAMA_URL = "http://localhost:11434/api/generate"

# def query_qwen(prompt, model="qwen2.5:0.5b"):
#     """Send a prompt to the local Ollama service and get the model's response"""
#     payload = {
#         "model": model,
#         "prompt": prompt,
#         "stream": False,  # one answer for one question
#         "options": {
#             "num_predict": 512  # limit response, reduce cost
#         }
#     }
#     try:
#         response = requests.post(OLLAMA_URL, json=payload, timeout=60)
#         response.raise_for_status()  # check status
#         return response.json()["response"]
#     except requests.exceptions.RequestException as e:
#         return f"调用本地模型时出错: {e}"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Define routing rules: agent type -> OpenRouter model
# Using "openrouter/free" for automatic free model selection
MODEL_ROUTING = {
    "coding":  {"model": "openrouter/free", "max_tokens": 1024},   # Programming expert
    "academic": {"model": "openrouter/free", "max_tokens": 2048}, # Academic expert
    "humanize": {"model": "openrouter/free", "max_tokens": 512}, # Text polishing expert
    "general": {"model": "openrouter/free", "max_tokens": 768},  # General assistant
}

def query_router(prompt, agent_type="general", retries=2):
    """Call different free models based on agent type via OpenRouter"""
    model = MODEL_ROUTING.get(agent_type, MODEL_ROUTING["general"])
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
    }
    for attempt in range(retries):
        try:
            response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
            print("DEBUG - Status Code:", response.status_code)
            print("DEBUG - Raw Response:", response.text)  # print orignal response
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            if attempt == retries - 1:
                return f"Model call failed: {e}"
            time.sleep(1)  # wait before retrying