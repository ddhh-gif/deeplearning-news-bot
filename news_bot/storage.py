from __future__ import annotations

from datetime import datetime
from pathlib import Path

from news_bot.models import DigestItem


def ensure_output_dir(output_dir: str) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def build_output_paths(output_dir: str, prefix: str = "arxiv_hparam_news") -> dict[str, Path]:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = ensure_output_dir(output_dir)
    return {
        "ini": out_dir / f"{prefix}_{ts}.ini",
        "md": out_dir / f"{prefix}_{ts}.md",
    }


def save_ini(items: list[DigestItem], path: Path, query: str) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write("[meta]\n")
        f.write(f"generated_at = {datetime.now().isoformat()}\n")
        f.write(f"total = {len(items)}\n")
        f.write(f"query = {query}\n\n")

        for i, item in enumerate(items, start=1):
            f.write(f"[paper_{i}]\n")
            f.write(f"title = {item.paper.title}\n")
            f.write(f"url = {item.paper.url}\n")
            f.write(f"relevance_score = {item.relevance_score}\n")
            f.write(f"keywords = {','.join(item.matched_keywords)}\n")
            f.write(f"published = {item.paper.published.isoformat() if item.paper.published else ''}\n")
            single_line_summary = item.summary.replace("\n", " ").strip()
            f.write(f"summary = {single_line_summary}\n\n")


def save_markdown(markdown_text: str, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(markdown_text)

