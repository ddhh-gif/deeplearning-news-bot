from __future__ import annotations

from argparse import ArgumentParser
from datetime import datetime
import sys

from news_bot.config import BotConfig
from news_bot.models import DigestItem
from news_bot.newsletter import render_markdown_newsletter
from news_bot.storage import build_output_paths, save_ini, save_markdown


def fallback_summary(abstract: str) -> str:
    text = " ".join(abstract.split())
    return (
        "一句话结论: 该论文可能与调参有关，但当前运行未启用 DeepSeek 总结。\n"
        f"调参要点: 摘要片段: {text[:240]}..."
    )


def run(config: BotConfig) -> None:
    from news_bot.fetchers.arxiv_source import fetch_recent_arxiv_papers
    from news_bot.filtering import rank_hyperparam_papers

    papers = fetch_recent_arxiv_papers(query=config.query, max_results=config.max_results)
    candidates = rank_hyperparam_papers(
        papers=papers,
        min_relevance_score=config.min_relevance_score,
        top_k=config.top_k,
    )

    summarizer = None
    if config.deepseek_api_key:
        from news_bot.summarizers.deepseek import DeepSeekSummarizer

        summarizer = DeepSeekSummarizer(
            api_key=config.deepseek_api_key,
            model=config.deepseek_model,
            base_url=config.deepseek_base_url,
        )

    digest_items: list[DigestItem] = []
    for item in candidates:
        print(f"处理论文: {item.paper.title}")
        if summarizer is not None:
            try:
                summary = summarizer.summarize_hyperparam_takeaways(
                    paper=item.paper,
                    matched_keywords=item.matched_keywords,
                )
            except Exception as exc:
                summary = f"一句话结论: 调用 DeepSeek 失败。\n调参要点: {exc}"
        else:
            summary = fallback_summary(item.paper.summary)

        digest_items.append(
            DigestItem(
                paper=item.paper,
                relevance_score=item.relevance_score,
                matched_keywords=item.matched_keywords,
                summary=summary,
            )
        )

    now = datetime.now()
    markdown_text = render_markdown_newsletter(
        items=digest_items,
        query=config.query,
        generated_at=now,
    )

    output_paths = build_output_paths(config.output_dir)
    save_markdown(markdown_text, output_paths["md"])
    save_ini(digest_items, output_paths["ini"], query=config.query)

    print(f"完成，共 {len(digest_items)} 篇")
    print(f"Markdown: {output_paths['md']}")
    print(f"INI: {output_paths['ini']}")


def parse_args() -> BotConfig:
    defaults = BotConfig.from_env()
    parser = ArgumentParser(description="Generate arXiv hyper-parameter newsletter.")
    parser.add_argument("--query", default=defaults.query)
    parser.add_argument("--max-results", type=int, default=defaults.max_results)
    parser.add_argument("--min-score", type=int, default=defaults.min_relevance_score)
    parser.add_argument("--top-k", type=int, default=defaults.top_k)
    parser.add_argument("--output-dir", default=defaults.output_dir)
    parser.add_argument("--model", default=defaults.deepseek_model)
    parser.add_argument("--base-url", default=defaults.deepseek_base_url)
    args = parser.parse_args()

    return BotConfig(
        query=args.query,
        max_results=args.max_results,
        min_relevance_score=args.min_score,
        top_k=args.top_k,
        output_dir=args.output_dir,
        deepseek_api_key=defaults.deepseek_api_key,
        deepseek_model=args.model,
        deepseek_base_url=args.base_url,
    )


if __name__ == "__main__":
    try:
        run(parse_args())
    except RuntimeError as exc:
        print(f"启动失败: {exc}")
        sys.exit(1)
