from __future__ import annotations

try:
    import arxiv
except ModuleNotFoundError as exc:  # pragma: no cover
    raise RuntimeError(
        "Missing dependency 'arxiv'. Install with: pip install -r requirements.txt"
    ) from exc

from news_bot.models import Paper


def fetch_recent_arxiv_papers(query: str, max_results: int = 30) -> list[Paper]:
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    client = arxiv.Client(page_size=min(max_results, 100), delay_seconds=3, num_retries=3)

    papers: list[Paper] = []
    for result in client.results(search):
        papers.append(
            Paper(
                title=result.title.strip(),
                summary=result.summary.strip(),
                url=result.entry_id,
                published=result.published,
                authors=[author.name for author in result.authors],
                source="arxiv",
            )
        )
    return papers
