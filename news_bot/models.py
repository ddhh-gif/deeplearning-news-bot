from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Paper:
    title: str
    summary: str
    url: str
    published: datetime | None
    authors: list[str] = field(default_factory=list)
    source: str = "arxiv"


@dataclass(slots=True)
class CandidatePaper:
    paper: Paper
    relevance_score: int
    matched_keywords: list[str]


@dataclass(slots=True)
class DigestItem:
    paper: Paper
    relevance_score: int
    matched_keywords: list[str]
    summary: str

