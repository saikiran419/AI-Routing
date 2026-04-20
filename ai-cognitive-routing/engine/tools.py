"""Phase 2 tools used inside LangGraph nodes."""

from typing import Dict, List

try:
    from langchain_core.tools import tool
except ImportError:
    def tool(func):  # type: ignore[misc]
        return func


@tool
def mock_searxng_search(query: str) -> List[Dict[str, str]]:
    """Mock search tool that returns deterministic snippets for a query."""
    lowered = query.lower()

    corpus = [
        {
            "title": "Developer productivity with AI copilots",
            "snippet": "Recent benchmarks show faster delivery for repetitive coding tasks.",
            "source": "mock://tech-journal",
        },
        {
            "title": "Junior developer role transformation",
            "snippet": "Teams are shifting junior roles toward review, testing, and prompt design.",
            "source": "mock://career-insights",
        },
        {
            "title": "Responsible adoption of generative AI",
            "snippet": "Organizations emphasize governance, human oversight, and staged rollout.",
            "source": "mock://ai-policy",
        },
    ]

    if "replace" in lowered or "junior" in lowered:
        return [corpus[1], corpus[0]]
    if "policy" in lowered or "ethics" in lowered or "safe" in lowered:
        return [corpus[2], corpus[1]]
    return [corpus[0], corpus[2]]
