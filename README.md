# AI Orchestrator - A Lightweight Multi-Agent Framework

This is a lightweight, local `AI Orchestrator` prototype built on top of Ollama. It demonstrates a clean architecture for **model routing (Router)**, **conversational memory (Memory)**, and **expert task delegation (Agents)**.

## Core Architecture
*   **Router**: A keyword-based dispatcher that intelligently routes user queries to the most relevant expert agent (e.g., Coding, Academic, Humanization).
*   **Expert Agents**: Specialized roles that use different system prompts to guide a single underlying LLM (Ollama) to perform distinct tasks.
*   **Memory Module**: A simple JSON-based persistent storage for conversation history, enabling short-term context retention.

## Requirements
*   Python 3.10+
*   [Ollama](https://ollama.com/) running locally with a model installed (e.g., `qwen2.5:0.5b`)

## Configuration
Create a `.env` file in the project root and add your OpenRouter API key:
`OPENROUTER_API_KEY=your_api_key_here`

## Quick Start
1.  Clone this repository.
2.  Install dependencies: `pip install requests`.
3.  Ensure your local Ollama service is running in the background (`ollama serve`).
4.  Run the orchestrator: `python main.py`.

## Project Highlights & Reflections
This project demonstrates a clean separation of concerns between orchestration (main.py), specialized agents (agents/), and model calling (llm_client.py). It showcases intelligent routing, context retrieval, and a lightweight review loop for multi-agent collaboration.

**Design Principles**: The architecture emphasizes system isolation (each agent operates independently without interference) and environmental consistency (API credentials and configurations are managed securely through .env file loading). This ensures stable execution across different deployment environments.

## Future Roadmap
*   Support for user-provided API keys (ChatGPT, Claude).

## Current Status (Phase 2 - Multi-Model Routing)
The orchestrator successfully routes queries to specialized agents (Coding, Academic, Humanize, General) and integrates a lightweight reviewer loop for quality control. Both OpenRouter (primary) and local Ollama (fallback) are now fully operational.