"""agent/graph.py — LangGraph agent graph definition.

Owner: Kunal.
Graph: Monitor -> Detect -> Retrieve -> Plan -> Verify -> Act -> (Recover on failure)
Streams TraceEvents via SSE for the frontend trace view.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from contracts.models import AgentRunRequest, TraceEvent

# TODO: Implement LangGraph state graph with nodes:
# - Monitor: entry for scheduled/on-demand runs
# - Detect: call get_risk, decide if action warranted
# - Retrieve: search_docs for guidance relevant to triggers
# - Plan: LLM drafts actions and messages
# - Verify: deterministic checks (numeric consistency, citations, banned content)
# - Act: persist agent_run, create alert, send Telegram, render evidence report
# - Recover: retry -> switch model -> templated output; mark DEGRADED


async def run_agent(request: AgentRunRequest) -> AsyncIterator[TraceEvent]:
    """Run the agent and yield trace events for SSE streaming."""
    raise NotImplementedError
