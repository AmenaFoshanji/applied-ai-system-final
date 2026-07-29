# Applied AI Documentation Assistant

## Slide 1 — Project Overview
- Evolved the original DocuBot into a more reliable applied AI system
- Helps developers answer questions from project documentation
- Focuses on grounded answers, guardrails, and evaluation

## Slide 2 — How the System Works
- User asks a question
- Retriever finds relevant documentation snippets
- RAG answer generator uses the retrieved evidence
- Guardrails refuse unsupported answers and keep responses safe

## Slide 3 — Demo and Evidence
- Run: `python main.py`
- Run: `pytest -q`
- Run: `python evaluation.py`
- Results: 4/4 tests passed and 7/8 retrieval checks hit the expected source

## Slide 4 — What I Learned
- AI systems are most useful when they are grounded and tested
- Guardrails and evaluation are essential for trustworthiness
- This project showed me how to build a practical AI workflow for real-world documentation tasks
