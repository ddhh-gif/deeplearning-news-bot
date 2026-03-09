from __future__ import annotations

from news_bot.models import CandidatePaper, Paper

HYPERPARAM_KEYWORDS: dict[str, int] = {
    "hyperparameter": 4,
    "hyper-parameter": 4,
    "hparam": 3,
    "tuning": 2,
    "search space": 2,
    "learning rate": 2,
    "batch size": 2,
    "weight decay": 2,
    "optimizer": 1,
    "scheduler": 1,
    "regularization": 1,
    "dropout": 1,
    "early stopping": 1,
    "grid search": 2,
    "bayesian optimization": 3,
    "parameter-efficient": 1,
}


def score_hyperparam_relevance(paper: Paper) -> tuple[int, list[str]]:
    text = f"{paper.title}\n{paper.summary}".lower()
    score = 0
    matched: list[str] = []

    for keyword, weight in HYPERPARAM_KEYWORDS.items():
        if keyword in text:
            score += weight
            matched.append(keyword)

    return score, matched


def rank_hyperparam_papers(
    papers: list[Paper],
    min_relevance_score: int = 2,
    top_k: int = 8,
) -> list[CandidatePaper]:
    candidates: list[CandidatePaper] = []
    for paper in papers:
        score, matched_keywords = score_hyperparam_relevance(paper)
        if score >= min_relevance_score:
            candidates.append(
                CandidatePaper(
                    paper=paper,
                    relevance_score=score,
                    matched_keywords=matched_keywords,
                )
            )

    candidates.sort(
        key=lambda item: (
            item.relevance_score,
            item.paper.published.isoformat() if item.paper.published else "",
        ),
        reverse=True,
    )
    return candidates[:top_k]

