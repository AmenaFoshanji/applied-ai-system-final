"""
Core DocuBot class responsible for:
- Loading documents from the docs/ folder
- Building a simple retrieval index (Phase 1)
- Retrieving relevant snippets (Phase 1)
- Supporting retrieval only answers
- Supporting RAG answers when paired with Gemini (Phase 2)
"""

import os
import glob
import re

class DocuBot:
    def __init__(self, docs_folder="docs", llm_client=None):
        """
        docs_folder: directory containing project documentation files
        llm_client: optional Gemini client for LLM based answers
        """
        self.docs_folder = docs_folder
        self.llm_client = llm_client

        # Load documents into memory
        self.documents = self.load_documents()  # List of (filename, text)

        # Split each document into smaller sections so retrieval can return
        # a focused snippet instead of a whole file.
        self.chunks = self.build_chunks()  # List of (filename, section_text)

        # Build a retrieval index (implemented in Phase 1)
        self.index = self.build_index(self.chunks)

    # -----------------------------------------------------------
    # Document Loading
    # -----------------------------------------------------------

    def load_documents(self):
        """
        Loads all .md and .txt files inside docs_folder.
        Returns a list of tuples: (filename, text)
        """
        docs = []
        pattern = os.path.join(self.docs_folder, "*.*")
        for path in glob.glob(pattern):
            if path.endswith(".md") or path.endswith(".txt"):
                with open(path, "r", encoding="utf8") as f:
                    text = f.read()
                filename = os.path.basename(path)
                docs.append((filename, text))
        return docs

    # -----------------------------------------------------------
    # Chunking: split documents into smaller sections
    # -----------------------------------------------------------

    def build_chunks(self):
        """
        Turn each (filename, full_text) document into several
        (filename, section_text) chunks so retrieval can pinpoint the
        relevant part of a file instead of returning the whole thing.
        """
        chunks = []
        for filename, text in self.documents:
            for section in self.chunk_document(text):
                chunks.append((filename, section))
        return chunks

    def chunk_document(self, text):
        """
        Split a Markdown document into sections at heading lines (lines
        starting with '#'). Each section keeps its heading together with
        the text that follows it, up to the next heading.

        Simple and consistent: no external libraries, just line scanning.
        """
        sections = []
        current = []
        for line in text.splitlines():
            # A heading starts a new section, but only once we've already
            # collected some lines (so the title isn't split off alone).
            if line.startswith("#") and current:
                sections.append("\n".join(current).strip())
                current = [line]
            else:
                current.append(line)
        if current:
            sections.append("\n".join(current).strip())

        # Drop any empty sections produced by blank runs.
        return [s for s in sections if s]

    # -----------------------------------------------------------
    # Index Construction (Phase 1)
    # -----------------------------------------------------------

    def build_index(self, documents):
        """
        TODO (Phase 1):
        Build a tiny inverted index mapping lowercase words to the documents
        they appear in.

        Example structure:
        {
            "token": ["AUTH.md", "API_REFERENCE.md"],
            "database": ["DATABASE.md"]
        }

        Keep this simple: split on whitespace, lowercase tokens,
        ignore punctuation if needed.
        """
        index = {}
        for filename, text in documents:
            for word in self.tokenize(text):
                docs_for_word = index.setdefault(word, [])
                if filename not in docs_for_word:
                    docs_for_word.append(filename)
        return index

    # Guardrail: a chunk must score at least this high to count as useful
    # context. Below it, matches are just incidental word overlap and the
    # bot should refuse rather than answer from noise.
    MIN_SCORE = 2

    # Common filler words that match everywhere and add noise to scoring.
    STOPWORDS = {
        "the", "is", "a", "an", "of", "to", "in", "on", "for", "and", "or",
        "how", "do", "i", "where", "which", "what", "are", "does", "all",
        "this", "that", "from", "with", "by", "be", "it",
    }

    def tokenize(self, text):
        """
        Split text into lowercase word tokens, dropping punctuation and
        common stopwords.
        "Which users?" -> ["users"]
        """
        words = re.findall(r"[a-z0-9]+", text.lower())
        kept = [w for w in words if w not in self.STOPWORDS]
        # Crude stemming: drop a trailing "s" so "endpoints" matches "endpoint".
        return [w[:-1] if w.endswith("s") and len(w) > 3 else w for w in kept]

    # -----------------------------------------------------------
    # Scoring and Retrieval (Phase 1)
    # -----------------------------------------------------------

    def score_document(self, query, text):
        """
        TODO (Phase 1):
        Return a simple relevance score for how well the text matches the query.

        Suggested baseline:
        - Convert query into lowercase words
        - Count how many appear in the text
        - Return the count as the score
        """
        query_words = set(self.tokenize(query))
        text_tokens = self.tokenize(text)
        # Count total occurrences: a doc that mentions a query word many
        # times is more relevant than one that mentions it once.
        return sum(text_tokens.count(word) for word in query_words)

    def retrieve(self, query, top_k=3):
        """
        TODO (Phase 1):
        Use the index and scoring function to select top_k relevant document snippets.

        Return a list of (filename, text) sorted by score descending.
        """
        scored = []
        for filename, chunk in self.chunks:
            score = self.score_document(query, chunk)
            # Guardrail: ignore weak matches. A chunk must clear MIN_SCORE
            # to count as "useful context." If nothing clears it, we return
            # an empty list and the caller refuses to answer.
            if score >= self.MIN_SCORE:
                scored.append((score, filename, chunk))

        scored.sort(key=lambda item: item[0], reverse=True)

        results = [(filename, chunk) for _, filename, chunk in scored]
        return results[:top_k]

    # -----------------------------------------------------------
    # Answering Modes
    # -----------------------------------------------------------

    def answer_retrieval_only(self, query, top_k=3):
        """
        Phase 1 retrieval only mode.
        Returns raw snippets and filenames with no LLM involved.
        """
        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        formatted = []
        for filename, text in snippets:
            formatted.append(f"[{filename}]\n{text}\n")

        return "\n---\n".join(formatted)

    def answer_rag(self, query, top_k=3):
        """
        Phase 2 RAG mode.
        Uses student retrieval to select snippets, then asks Gemini
        to generate an answer using only those snippets.
        """
        if self.llm_client is None:
            raise RuntimeError(
                "RAG mode requires an LLM client. Provide a GeminiClient instance."
            )

        snippets = self.retrieve(query, top_k=top_k)

        if not snippets:
            return "I do not know based on these docs."

        return self.llm_client.answer_from_snippets(query, snippets)

    # -----------------------------------------------------------
    # Bonus Helper: concatenated docs for naive generation mode
    # -----------------------------------------------------------

    def full_corpus_text(self):
        """
        Returns all documents concatenated into a single string.
        This is used in Phase 0 for naive 'generation only' baselines.
        """
        return "\n\n".join(text for _, text in self.documents)
