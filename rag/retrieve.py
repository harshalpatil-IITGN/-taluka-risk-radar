"""rag/retrieve.py — Document retrieval with cosine similarity and abstain threshold.

Owner: Kunal.
If best score < threshold, agent says "no official guidance found".
"""

from __future__ import annotations

from contracts.models import DocHit

# TODO: Implement
# - Embed query with multilingual-e5-small
# - Cosine similarity search via db.repo.search_doc_chunks
# - Low-score abstain threshold
# - Return list[DocHit] with title/url/page


def search_docs(query: str, k: int = 5, lang: str | None = None) -> list[DocHit]:
    """Search the document corpus and return top-k hits."""
    raise NotImplementedError
