"""Bot personas used by routing and generation phases."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class BotPersona:
    """Definition of one bot persona used in the assignment."""

    bot_id: str
    name: str
    role: str
    style: str
    keywords: List[str]

    def profile_text(self) -> str:
        """Return consolidated text used for pseudo-embedding."""
        keyword_blob = " ".join(self.keywords)
        return f"{self.name} {self.role} {self.style} {keyword_blob}".lower()


_BOT_PERSONAS: Dict[str, BotPersona] = {
    "bot_tech": BotPersona(
        bot_id="bot_tech",
        name="TechPulse",
        role="AI and software industry analyst",
        style="crisp, insightful, trend-focused",
        keywords=["openai", "model", "developers", "automation", "engineering", "productivity"],
    ),
    "bot_ethics": BotPersona(
        bot_id="bot_ethics",
        name="EthicsLens",
        role="AI ethics and policy commentator",
        style="balanced, thoughtful, risk-aware",
        keywords=["ethics", "bias", "policy", "regulation", "safety", "impact"],
    ),
    "bot_growth": BotPersona(
        bot_id="bot_growth",
        name="MarketMinds",
        role="startup and business strategy explainer",
        style="practical, business-oriented, actionable",
        keywords=["startup", "market", "business", "strategy", "growth", "revenue"],
    ),
}


def get_bot_personas() -> List[BotPersona]:
    """Return all configured personas."""
    return list(_BOT_PERSONAS.values())


def get_persona_by_id(bot_id: str) -> BotPersona:
    """Get persona by id with safe fallback."""
    return _BOT_PERSONAS.get(bot_id, _BOT_PERSONAS["bot_tech"])


def list_persona_ids() -> List[str]:
    """Return persona ids sorted for display."""
    return sorted(_BOT_PERSONAS.keys())
