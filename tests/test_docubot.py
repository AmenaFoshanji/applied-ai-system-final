import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docubot import DocuBot


def test_retrieve_returns_relevant_snippets():
    bot = DocuBot(docs_folder="docs")
    snippets = bot.retrieve("How do I connect to the database?", top_k=3)
    assert snippets
    assert any("DATABASE.md" in filename for filename, _ in snippets)


def test_retrieval_only_refuses_when_no_match():
    bot = DocuBot(docs_folder="docs")
    answer = bot.answer_retrieval_only("What about purple dragons in space?")
    assert "I do not know" in answer


def test_full_corpus_contains_docs():
    bot = DocuBot(docs_folder="docs")
    text = bot.full_corpus_text()
    assert "Authentication" in text or "Database" in text


def test_rag_falls_back_gracefully_without_llm():
    bot = DocuBot(docs_folder="docs")
    answer = bot.answer_rag("How do I connect to the database?")
    assert "language model" in answer.lower() or "I do not know" in answer
