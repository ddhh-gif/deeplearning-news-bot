from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(slots=True)
class BotConfig:
    query: str = "(deep learning) AND (hyperparameter OR tuning OR learning rate OR batch size)"
    max_results: int = 30
    min_relevance_score: int = 2
    top_k: int = 8
    output_dir: str = "output"
    deepseek_api_key: str | None = None
    deepseek_model: str = "deepseek-chat"
    deepseek_base_url: str = "https://api.deepseek.com"

    @classmethod
    def from_env(cls) -> "BotConfig":
        return cls(
            query=os.getenv(
                "NEWS_QUERY",
                "(deep learning) AND (hyperparameter OR tuning OR learning rate OR batch size)",
            ),
            max_results=int(os.getenv("NEWS_MAX_RESULTS", "30")),
            min_relevance_score=int(os.getenv("NEWS_MIN_SCORE", "2")),
            top_k=int(os.getenv("NEWS_TOP_K", "8")),
            output_dir=os.getenv("NEWS_OUTPUT_DIR", "output"),
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
            deepseek_model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            deepseek_base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        )

