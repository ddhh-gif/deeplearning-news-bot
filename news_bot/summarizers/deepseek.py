from __future__ import annotations

try:
    from openai import OpenAI
except ModuleNotFoundError as exc:  # pragma: no cover
    raise RuntimeError(
        "Missing dependency 'openai'. Install with: pip install -r requirements.txt"
    ) from exc

from news_bot.models import Paper


class DeepSeekSummarizer:
    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
    ) -> None:
        if not api_key:
            raise ValueError("Missing API key for DeepSeek.")
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def summarize_hyperparam_takeaways(self, paper: Paper, matched_keywords: list[str]) -> str:
        keywords = ", ".join(matched_keywords) if matched_keywords else "not explicitly stated"
        prompt = f"""
你是一位机器学习研究速递编辑。请阅读论文标题和摘要，给出调参相关结论。

论文标题: {paper.title}
关键词命中: {keywords}
摘要: {paper.summary}

请严格使用下面格式输出，不要加额外说明:
一句话结论: <一句话>
调参要点: <1-2句，尽量写 learning rate / batch size / optimizer 等可执行建议；如果没有明确内容写"摘要未提及">
实验发现: <1句，强调对性能或稳定性的影响；如果没有明确内容写"摘要未提及">
局限性: <1句，如摘要未提及则写"摘要未提及">
"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=360,
        )
        return response.choices[0].message.content.strip()
