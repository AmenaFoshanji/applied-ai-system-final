# Applied AI Documentation Assistant

## Original Project Context

This project is an evolution of the Module 4 DocuBot starter project. Its original goal was to help developers ask questions about project documentation by searching a small set of markdown files. The original system was a lightweight prototype for retrieval and answer generation, and this version extends that idea into a more complete applied AI system with stronger grounding, safer behavior, and clearer evaluation.

## What the project does

This project turns documentation into a practical AI assistant that can answer developer questions using evidence from the project docs. It is designed to help someone quickly find answers about authentication, database setup, API routes, and other important project details without relying on guesswork.

## Why it matters

In real-world teams, documentation is often scattered and incomplete. This system makes documentation more accessible by combining retrieval, AI-generated answers, and guardrails so the assistant can provide useful help while still being careful about uncertainty.

## Architecture overview

The system follows a simple retrieval-augmented generation pipeline:

1. A user asks a question.
2. The retriever searches the documentation corpus for relevant snippets.
3. The answer generator uses those snippets as evidence.
4. Guardrails check the result for reliability and avoid unsupported claims.
5. If no LLM is available, the system falls back to a grounded retrieval summary instead of hallucinating.

The Mermaid diagram for this architecture is stored in [diagrams/architecture.mmd](diagrams/architecture.mmd).

## Setup instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file with your Gemini API key:

```bash
GEMINI_API_KEY=your_api_key_here
```

If you do not provide a Gemini key, the assistant can still run in retrieval-only or grounded fallback mode.

### 3. Run the application

```bash
python main.py
```

Choose one of the following modes:
- 1: Naive LLM over the full docs
- 2: Retrieval-only mode
- 3: RAG mode with grounded retrieval

### 4. Run tests

```bash
pytest -q
```

## Sample interactions

### Example 1

Input:
```text
How do I connect to the database?
```

Output:
```text
The assistant retrieves the database documentation and returns a grounded answer that references the relevant snippet.
```

### Example 2

Input:
```text
Where is the auth token generated?
```

Output:
```text
The assistant searches the authentication docs and returns the relevant evidence-based explanation.
```

### Example 3

Input:
```text
What about purple dragons in space?
```

Output:
```text
The assistant refuses to answer with unsupported information and returns a safe fallback message.
```

## Design decisions

I built the system this way because a documentation assistant is more useful when it is grounded in evidence rather than simply generating text from memory. The retrieval layer helps focus the response, while the guardrails make the assistant more trustworthy. A trade-off of this design is that it is intentionally conservative; sometimes it refuses to answer when the evidence is weak, but that is preferable to giving a confident but incorrect answer.

## Testing summary

The project includes automated tests for core retrieval behavior and fallback handling. Verified results: 4 out of 4 tests passed, and the system successfully handled unsupported questions by refusing to guess. The assistant also logs retrieval and generation events so failures can be traced and improved.

### Structured evaluation

| Test input | Evaluation criteria | Result |
| --- | --- | --- |
| How do I connect to the database? | Returns a relevant, evidence-based answer | Pass |
| Where is the auth token generated? | Returns a relevant, evidence-based answer | Pass |
| What about purple dragons in space? | Handles gracefully and refuses unsupported answers | Pass |

## Reflection

This project taught me that the most useful AI systems are not just clever — they are dependable. Designing for grounding, testing, and safe failure modes is often more important than maximizing raw output quality. I also learned that good AI engineering requires balancing usefulness with caution, especially when users may assume the system is always correct.

## Requirements

- Python 3.9+
- Gemini API key for LLM-backed modes (optional for fallback mode)
