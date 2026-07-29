# Applied AI Documentation Assistant

## Slide 1 — Project Overview
- Introduce the problem: developers often struggle to find answers quickly in scattered documentation
- Present the solution: a documentation assistant that retrieves evidence and answers questions safely
- Emphasize the goal: turn a prototype into a more trustworthy applied AI system

## Slide 2 — How the System Works
- A user asks a question
- The retriever finds relevant documentation snippets
- The RAG layer uses those snippets to generate a grounded response
- Guardrails prevent unsupported claims and provide a safe fallback when evidence is weak

## Slide 3 — Demo and Evidence
- Show the main command: `python main.py`
- Show the reliability checks: `pytest -q`
- Show the evaluation harness: `python evaluation.py`
- Mention the verified results: 4/4 tests passed and 7/8 retrieval checks hit the expected source

## Slide 4 — What I Learned and Why It Matters
- AI is most valuable when it is grounded, tested, and transparent
- Guardrails and evaluation are essential to build trust in real-world systems
- This project taught me how to move from a simple prototype to a more practical and responsible AI workflow
