"""rag/ingest.py — Ingest official PDFs, chunk, embed, and store.

Owner: Kunal.
Corpus: Drought Manual, CRIDA DACPs, SAU advisories, PMFBY guidelines.
"""

from __future__ import annotations

# TODO: Implement
# - Download PDFs from official sources
# - Chunk by section/page (~300-500 tokens)
# - Embed with multilingual-e5-small (384-d)
# - Store in doc_chunk table via db.repo.upsert_doc_chunks
