# DL Hyper-Param News Bot

自动抓取 arXiv 论文，筛选 DL 调参相关内容，并输出 newsletter（Markdown + INI）。

## 安装

```bash
pip install -r requirements.txt
```

## 配置

使用环境变量注入 DeepSeek key，不要写在代码里。

```bash
export DEEPSEEK_API_KEY="your_key"
```

可选配置：

- `NEWS_QUERY`
- `NEWS_MAX_RESULTS`
- `NEWS_MIN_SCORE`
- `NEWS_TOP_K`
- `NEWS_OUTPUT_DIR`
- `DEEPSEEK_MODEL`（默认 `deepseek-chat`）
- `DEEPSEEK_BASE_URL`（默认 `https://api.deepseek.com`）

## 网络配置（SOCKS5 / 关闭 TUN mode）

如果你的网络环境需要代理，建议优先使用 `SOCKS5` 端口，并关闭代理软件的 `TUN mode`（避免全局路由接管导致 Python/SSL/DNS 异常）。

示例（将端口替换为你本地实际端口，例如 `7890`）：

```bash
export ALL_PROXY="socks5h://127.0.0.1:7890"
export HTTP_PROXY="socks5h://127.0.0.1:7890"
export HTTPS_PROXY="socks5h://127.0.0.1:7890"
```

### 端口对 pip 的影响（常见坑）

`pip install -r requirements.txt` 也会走上面的代理端口。端口配置不对时，最先失败的通常就是 `pip`。

常见报错和原因：

- `Connection refused` / `Cannot connect to proxy`: 端口写错，或代理软件没启动
- `Read timed out`: 端口可用但线路慢，或网络策略拦截
- `SOCKS support` 相关报错: 当前 Python 环境缺少 SOCKS 依赖（可尝试安装 `pysocks`）
- `SSL: CERTIFICATE_VERIFY_FAILED`: 证书链问题（公司网/校园网常见）

建议排查顺序：

1. 先确认代理软件在本机监听的真实端口（不确定就去软件设置里看）
2. 确认终端里 `ALL_PROXY/HTTP_PROXY/HTTPS_PROXY` 和该端口一致
3. 再执行 `pip install -r requirements.txt`
4. 仍失败就把完整报错贴给 AI（不要只截最后一行）

**说明：这部分网络配置只覆盖常见情况，作者不熟悉复杂网络环境；如果你使用公司网、校园网或自定义网关，建议继续向 AI 提问做针对性排查。（作者太菜了）**

## 运行

```bash
python main.py
```

可覆盖参数：

```bash
python main.py --query "(deep learning) AND (learning rate OR batch size)" --max-results 40 --top-k 10
```

输出位于 `output/`，包括：

- `*.md` newsletter 人类可读版
- `*.ini` 程序消费版

## 代码结构

- `main.py`: 入口和流程编排
- `news_bot/fetchers/arxiv_source.py`: arXiv 拉取
- `news_bot/filtering.py`: hyper-parameter 相关性打分/筛选
- `news_bot/summarizers/deepseek.py`: DeepSeek 总结
- `news_bot/newsletter.py`: Markdown newsletter 渲染
- `news_bot/storage.py`: INI/Markdown 持久化
