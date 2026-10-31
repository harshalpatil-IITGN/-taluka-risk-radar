"""agent/guardrails.py — Content guardrails for agent outputs.

Owner: Kunal.
"""

from __future__ import annotations

# TODO: Implement guardrails:
# - No pesticide/fertiliser dosages
# - No seed-variety endorsements without citation
# - No buy/sell/hold advice (show price vs MSP as information only)
# - Refuse out-of-scope questions (politics, medical, etc.)
# - Language must match user's request
# - Numbers must match tool outputs exactly
# - Stale/missing data: first line disclaimer, lower confidence
# - Farmer-distress statistics never in generated advisories
