from news_bot.fetchers.arxiv_source import fetch_recent_arxiv_papers


def main() -> None:
    papers = fetch_recent_arxiv_papers(
        query="(deep learning) AND (hyperparameter OR tuning)",
        max_results=5,
    )
    for idx, paper in enumerate(papers, start=1):
        print(f"{idx}. {paper.title}")
        print(f"   {paper.url}")


if __name__ == "__main__":
    main()
