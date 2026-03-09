from __future__ import annotations

from datetime import datetime

from news_bot.models import DigestItem


def render_markdown_newsletter(
    items: list[DigestItem],
    query: str,
    generated_at: datetime,
) -> str:
    lines: list[str] = []
    lines.append("# DL Hyper-Parameter News")
    lines.append("")
    lines.append(f"- Generated at: {generated_at.isoformat(timespec='seconds')}")
    lines.append(f"- Query: `{query}`")
    lines.append(f"- Total papers: {len(items)}")
    lines.append("")

    if not items:
        lines.append("No relevant papers found for this run.")
        return "\n".join(lines)

    for idx, item in enumerate(items, start=1):
        lines.append(f"## {idx}. {item.paper.title}")
        lines.append(f"- Link: {item.paper.url}")
        lines.append(f"- Relevance score: {item.relevance_score}")
        lines.append(f"- Matched keywords: {', '.join(item.matched_keywords) or 'N/A'}")
        lines.append(f"- Published: {item.paper.published.isoformat() if item.paper.published else 'N/A'}")
        lines.append("")
        lines.append(item.summary)
        lines.append("")

    return "\n".join(lines)

