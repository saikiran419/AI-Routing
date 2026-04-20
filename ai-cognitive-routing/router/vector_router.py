"""Phase 1: Persona routing using pseudo-embeddings and vector search."""

from dataclasses import dataclass
import math
import re
from typing import Dict, List, Tuple

from data.personas import BotPersona, get_bot_personas


def _tokenize(text: str) -> List[str]:
    """Convert text into normalized tokens."""
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def _build_vocabulary(personas: List[BotPersona]) -> List[str]:
    """Build a stable vocabulary from persona profiles."""
    vocab_set = set()
    for persona in personas:
        vocab_set.update(_tokenize(persona.profile_text()))
    return sorted(vocab_set)


def _text_to_embedding(text: str, vocabulary: List[str]) -> List[float]:
    """Create a deterministic bag-of-words embedding vector."""
    tokens = _tokenize(text)
    counts: Dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1

    vector = [float(counts.get(word, 0)) for word in vocabulary]
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(a) != len(b) or len(a) == 0:
        return 0.0
    return sum(x * y for x, y in zip(a, b))


@dataclass
class PersonaVectorRecord:
    """Stored vector record for one persona."""

    bot_id: str
    embedding: List[float]
    keywords: List[str]


class InMemoryVectorDB:
    """Tiny in-memory vector DB used for assignment demonstration."""

    def __init__(self) -> None:
        self.records: List[PersonaVectorRecord] = []

    def upsert(self, record: PersonaVectorRecord) -> None:
        """Insert or replace a record by bot id."""
        self.records = [existing for existing in self.records if existing.bot_id != record.bot_id]
        self.records.append(record)

    def query(self, embedding: List[float]) -> List[Tuple[PersonaVectorRecord, float]]:
        """Return records sorted by similarity descending."""
        scored = []
        for record in self.records:
            similarity = _cosine_similarity(embedding, record.embedding)
            scored.append((record, similarity))
        return sorted(scored, key=lambda item: item[1], reverse=True)


@dataclass
class RouteResult:
    """Result of routing a post to the most relevant bot."""

    bot_id: str
    score: float
    matched_keywords: List[str]
    above_threshold: bool


_PERSONAS = get_bot_personas()
_VOCABULARY = _build_vocabulary(_PERSONAS)
_VECTOR_DB = InMemoryVectorDB()

for _persona in _PERSONAS:
    _VECTOR_DB.upsert(
        PersonaVectorRecord(
            bot_id=_persona.bot_id,
            embedding=_text_to_embedding(_persona.profile_text(), _VOCABULARY),
            keywords=_persona.keywords,
        )
    )


def route_post_to_bots(post_content: str, threshold: float = 0.85) -> RouteResult:
    """Route post content to the best matching bot persona."""
    post_embedding = _text_to_embedding(post_content, _VOCABULARY)
    top_record, cosine_score = _VECTOR_DB.query(post_embedding)[0]

    post_text = post_content.lower()
    matched_keywords = [word for word in top_record.keywords if word in post_text]
    heuristic_score = 0.55 + (0.12 * len(matched_keywords))
    final_score = min(0.99, max(cosine_score, heuristic_score))

    return RouteResult(
        bot_id=top_record.bot_id,
        score=round(final_score, 3),
        matched_keywords=matched_keywords,
        above_threshold=final_score >= threshold,
    )
