"""Phase 2: LangGraph content generation pipeline."""

import json
from typing import Dict, List, TypedDict

from data.personas import get_persona_by_id
from engine.tools import mock_searxng_search

try:
    from langgraph.graph import END, StateGraph
    HAS_LANGGRAPH = True
except ImportError:
    END = "END"
    HAS_LANGGRAPH = False


class PostState(TypedDict):
    """Workflow state for content generation graph."""

    bot_id: str
    topic: str
    needs_search: bool
    search_results: List[Dict[str, str]]
    post_content: str


def decide_search_node(state: PostState) -> PostState:
    """Node 1: Decide if topic needs web search before drafting."""
    topic = state["topic"].lower()
    needs_search = any(token in topic for token in ["new", "released", "trend", "impact", "replace"]) 

    return {
        **state,
        "needs_search": needs_search,
        "search_results": [],
    }


def web_search_node(state: PostState) -> PostState:
    """Node 2: Run mock web search when needed."""
    if not state["needs_search"]:
        return state

    if hasattr(mock_searxng_search, "invoke"):
        results = mock_searxng_search.invoke(state["topic"])
    else:
        results = mock_searxng_search(state["topic"])

    return {
        **state,
        "search_results": results,
    }


def draft_post_node(state: PostState) -> PostState:
    """Node 3: Draft final social post content from topic and context."""
    persona = get_persona_by_id(state["bot_id"])

    context_line = ""
    if state["search_results"]:
        top = state["search_results"][0]
        context_line = f" Evidence: {top['snippet']}"

    drafted = (
        f"[{persona.name}] {state['topic']}. "
        f"Takeaway: teams should adapt skills, not panic.{context_line}"
    )

    return {
        **state,
        "post_content": drafted,
    }


def _run_without_langgraph(initial_state: PostState) -> PostState:
    """Fallback sequential execution when LangGraph isn't installed."""
    state = decide_search_node(initial_state)
    state = web_search_node(state)
    state = draft_post_node(state)
    return state


def _build_graph():
    """Build and compile assignment graph with three nodes."""
    graph = StateGraph(PostState)
    graph.add_node("Decide Search", decide_search_node)
    graph.add_node("Web Search", web_search_node)
    graph.add_node("Draft Post", draft_post_node)

    graph.set_entry_point("Decide Search")
    graph.add_edge("Decide Search", "Web Search")
    graph.add_edge("Web Search", "Draft Post")
    graph.add_edge("Draft Post", END)
    return graph.compile()


def generate_post_with_langgraph(bot_id: str, topic: str) -> Dict[str, str]:
    """Generate post content and return required JSON payload fields."""
    initial_state: PostState = {
        "bot_id": bot_id,
        "topic": topic,
        "needs_search": False,
        "search_results": [],
        "post_content": "",
    }

    if HAS_LANGGRAPH:
        app = _build_graph()
        final_state = app.invoke(initial_state)
    else:
        final_state = _run_without_langgraph(initial_state)

    return {
        "bot_id": final_state["bot_id"],
        "topic": final_state["topic"],
        "post_content": final_state["post_content"],
    }


def generate_post_json(bot_id: str, topic: str) -> str:
    """Return assignment-required JSON output string."""
    payload = generate_post_with_langgraph(bot_id=bot_id, topic=topic)
    return json.dumps(payload, ensure_ascii=True)
