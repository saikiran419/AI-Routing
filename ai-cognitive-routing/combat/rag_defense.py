"""Phase 3: RAG defense reply generation with injection filtering."""

from dataclasses import dataclass
import re
from typing import List, Tuple


@dataclass
class SafetyReport:
    """Safety scan output for user text."""

    sanitized_text: str
    blocked: bool
    reasons: List[str]


def _detect_injection(text: str) -> List[str]:
    """Detect prompt-injection markers in text."""
    checks: List[Tuple[str, str]] = [
        ("instruction override", r"ignore\s+all\s+previous\s+instructions"),
        ("instruction override", r"ignore\s+previous\s+instructions"),
        ("system prompt extraction", r"reveal\s+(the\s+)?system\s+prompt"),
        ("jailbreak attempt", r"act\s+as\s+if\s+there\s+are\s+no\s+rules"),
    ]

    matched: List[str] = []
    for reason, pattern in checks:
        if re.search(pattern, text, flags=re.IGNORECASE):
            matched.append(reason)
    return matched


def evaluate_text_safety(text: str) -> SafetyReport:
    """Sanitize input and decide whether to block response generation."""
    stripped = text.strip()
    reasons = _detect_injection(stripped)
    blocked = len(reasons) > 0

    sanitized = stripped
    for pattern in [r"ignore\s+all\s+previous\s+instructions", r"ignore\s+previous\s+instructions"]:
        sanitized = re.sub(pattern, "[BLOCKED_INJECTION]", sanitized, flags=re.IGNORECASE)

    return SafetyReport(sanitized_text=sanitized, blocked=blocked, reasons=reasons)


def _build_context_blob(parent_post: str, comment_history: List[str]) -> str:
    """Build compact RAG-style context from parent post and comments."""
    latest_comments = comment_history[-5:]
    history_text = " | ".join(latest_comments) if latest_comments else "No previous comments"
    return f"Parent: {parent_post} || History: {history_text}"


def generate_defense_reply(
    bot_persona: str,
    parent_post: str,
    comment_history: List[str],
    human_reply: str,
) -> str:
    """Generate a safe reply grounded in thread context with injection defense."""
    safety = evaluate_text_safety(human_reply)

    if safety.blocked:
        return (
            f"[{bot_persona}] I cannot follow instruction-override requests. "
            "Please ask a normal question related to the discussion."
        )

    context_blob = _build_context_blob(parent_post, comment_history)

    return (
        f"[{bot_persona}] Thanks for your comment. Based on thread context, "
        f"the key point is to adapt skills while keeping human review in the loop. "
        f"Your reply was: '{safety.sanitized_text}'. "
        f"Context used: {context_blob}"
    )
