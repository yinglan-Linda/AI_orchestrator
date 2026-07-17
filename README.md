# AI Orchestrator - A Lightweight Multi-Agent Framework

This is a lightweight, local `AI Orchestrator` prototype built on top of Ollama. It demonstrates a clean architecture for **model routing (Router)**, **conversational memory (Memory)**, and **expert task delegation (Agents)**.

## Core Architecture
*   **Router**: A keyword-based dispatcher that intelligently routes user queries to the most relevant expert agent (e.g., Coding, Academic, Humanization, Search).
*   **Expert Agents**: Specialized roles that use different system prompts to guide a single underlying LLM (Ollama) to perform distinct tasks.
*   **Memory Module**: A simple JSON-based persistent storage for conversation history, enabling short-term context retention.

## Requirements
*   Python 3.10+
*   [Ollama](https://ollama.com/) running locally with a model installed (e.g., `qwen2.5:0.5b`)

## Quick Start
1.  Clone this repository.
2.  Install dependencies: `pip install requests`.
3.  Ensure your local Ollama service is running in the background (`ollama serve`).
4.  Run the orchestrator: `python src/main.py`.

## Project Highlights & Reflections
This project was designed and tested within a Debian virtual machine environment. The key engineering considerations were **system isolation** and **environmental consistency** to guarantee stable execution of the AI Orchestrator. I also encountered and resolved challenges related to LVM disk expansion, which deepened my hands-on understanding of Linux storage management and system recovery processes.

## Future Roadmap
*   Integration with OpenRouter for free access to multiple models (DeepSeek, Gemma, etc.).
*   Implementation of a reflective loop (Reviewer Agent) for self-correction.
*   Support for user-provided API keys (ChatGPT, Claude).