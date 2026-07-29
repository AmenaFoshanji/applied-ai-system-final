# Applied AI Documentation Assistant

This project evolves a simple documentation chatbot into a more useful applied AI system. It helps developers answer questions about project documentation by combining retrieval, grounded reasoning, and guardrails.

## What the system does

The assistant can:
- retrieve relevant documentation snippets from the project docs
- answer questions using a retrieval-augmented generation (RAG) workflow
- fall back safely when no language model is available
- log important events and avoid guessing when evidence is weak

## AI features included

- Retrieval-Augmented Generation (RAG): the assistant retrieves evidence before answering
- Reliability and guardrails: it refuses to answer when it has insufficient evidence
- Logging: the system records retrieval and generation events for transparency

## Project structure

- `docubot.py` — retrieval, chunking, scoring, and grounded response logic
- `llm_client.py` — Gemini integration and safe prompt handling
- `main.py` — command-line interface for running the assistant
- `tests/` — regression tests for retrieval and fallback behavior
- `diagrams/architecture.mmd` — Mermaid architecture diagram
- `assets/` — supporting images and visuals

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file with your Gemini API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

If no Gemini key is provided, the assistant can still run in retrieval-only or grounded fallback mode.

## Run the application

```bash
python main.py
```

Choose one of the following modes:
- 1: Naive LLM over the full docs
- 2: Retrieval-only mode
- 3: RAG mode with grounded retrieval

## Run tests

```bash
pytest -q
```

## Responsible design notes

The assistant is designed to be cautious. It uses retrieved snippets as evidence, refuses to invent answers, and provides a safe fallback when no LLM is available.

## Requirements

- Python 3.9+
- Gemini API key for LLM-backed modes (optional for fallback mode)
