from __future__ import annotations

import asyncio
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .models import CrawlArtifacts
from .parsers import (
    choose_complete_transcript_payload,
    is_renderable_document_block,
    parse_document_blocks,
    parse_number,
    parse_transcript,
)


ALLOWED_HOSTS = {"feishu.doubao.com"}
CHROME_CANDIDATES = (
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/google-chrome-stable"),
)


DOCUMENT_SCROLL_SCRIPT = r"""
const iframe = [...document.querySelectorAll('iframe')]
  .find(item => (item.src || '').includes('/partner/ccm-docx/docx/'));
if (!iframe || !iframe.contentDocument) {
  return { error: '文档 iframe 不可用', blocks: [] };
}
const doc = iframe.contentDocument;
const win = iframe.contentWindow;
const all = [...doc.querySelectorAll('*')];
const container = all.find(element => {
  const style = win.getComputedStyle(element);
  return ['auto', 'scroll'].includes(style.overflowY)
    && element.scrollHeight > element.clientHeight + 100;
});
if (!container) {
  return { error: '未找到文档虚拟滚动容器', blocks: [] };
}

const found = new Map();
const samples = [];
let y = 0;
let stableBottomRounds = 0;
let lastHeight = 0;
let observationOrder = 0;
const step = Math.max(350, Math.floor(container.clientHeight * 0.65));

function collectBlocks() {
  let elements = [...doc.querySelectorAll('[data-block-id]')];
  if (!elements.length) {
    elements = [...doc.querySelectorAll('[id^="doxcn"]')];
  }
  const containerTop = container.getBoundingClientRect().top;
  for (const element of elements) {
    const blockId = element.getAttribute('data-block-id') || element.id;
    if (!blockId) continue;
    const parent = element.parentElement?.closest('[data-block-id],[id^="doxcn"]');
    const text = (element.innerText || '').replace(/\u200b/g, '').trim();
    const top = Math.round(
      element.getBoundingClientRect().top - containerTop + container.scrollTop
    );
    const candidate = {
      block_id: blockId,
      order: observationOrder++,
      top,
      tag: element.tagName,
      css_class: String(element.className || ''),
      text,
      outer_html: element.outerHTML || '',
      parent_block_id: parent
        ? (parent.getAttribute('data-block-id') || parent.id || null)
        : null,
    };
    const current = found.get(blockId);
    if (!current || candidate.text.length > current.text.length) {
      found.set(blockId, candidate);
    }
  }
  return elements.length;
}

for (let index = 0; index < 40; index += 1) {
  const height = container.scrollHeight;
  const maxScroll = Math.max(0, height - container.clientHeight);
  y = Math.min(index === 0 ? 0 : y + step, maxScroll);
  container.scrollTop = y;
  container.dispatchEvent(new Event('scroll'));
  await new Promise(resolve => setTimeout(resolve, 500));
  const domBlockCount = collectBlocks();
  const nextHeight = container.scrollHeight;
  const nextMaxScroll = Math.max(0, nextHeight - container.clientHeight);
  const atBottom = container.scrollTop >= nextMaxScroll - 5;
  stableBottomRounds = atBottom && nextHeight === lastHeight
    ? stableBottomRounds + 1
    : 0;
  lastHeight = nextHeight;
  samples.push({
    index,
    scroll_top: container.scrollTop,
    scroll_height: nextHeight,
    max_scroll: nextMaxScroll,
    at_bottom: atBottom,
    dom_block_count: domBlockCount,
  });
  if (stableBottomRounds >= 2) break;
  if (atBottom) y = Math.max(0, y - step);
}

const blocks = [...found.values()].sort((left, right) =>
  left.top - right.top || left.order - right.order || left.block_id.localeCompare(right.block_id)
);
const joinedText = blocks.map(item => item.text).join('\n');
const finalMaxScroll = Math.max(0, container.scrollHeight - container.clientHeight);
const lastSample = samples[samples.length - 1];
container.scrollTop = 0;

return {
  title: doc.title || document.title || '',
  iframe_ready_state: doc.readyState,
  final_scroll_height: container.scrollHeight,
  client_height: container.clientHeight,
  final_max_scroll: finalMaxScroll,
  bottom_reached: Boolean(lastSample?.at_bottom && stableBottomRounds >= 2),
  stable_bottom_rounds: stableBottomRounds,
  samples,
  blocks,
  unique_block_count: blocks.length,
  nonempty_block_count: blocks.filter(item => item.text).length,
  heading_coverage: {
    summary: joinedText.includes('总结'),
    chapters: joinedText.includes('智能章节'),
    decisions: joinedText.includes('关键决策'),
    quotes: joinedText.includes('金句时刻'),
  },
};
"""


@dataclass(frozen=True)
class CrawlOptions:
    headless: bool = True
    delay_before_extract: float = 10.0
    page_timeout_ms: int = 120_000
    user_agent: str | None = None
    storage_state: Path | None = None


def validate_source_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("仅允许抓取 https://feishu.doubao.com 下的已授权文档")
    if not re.fullmatch(r"/docx/[A-Za-z0-9]+/?", parsed.path):
        raise ValueError("URL 必须是飞书豆包 docx 文档链接")
    return url


def detect_chrome_version() -> tuple[Path, str]:
    for executable in CHROME_CANDIDATES:
        if not executable.is_file():
            continue
        completed = subprocess.run(
            [str(executable), "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", completed.stdout)
        if match:
            return executable, match.group(1)
    raise RuntimeError("未找到可用的 Google Chrome，无法构造真实 User-Agent")


def chrome_user_agent(version: str) -> str:
    if not re.fullmatch(r"\d+\.\d+\.\d+\.\d+", version):
        raise ValueError(f"无效 Chrome 版本：{version}")
    return (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{version} Safari/537.36"
    )


def _js_result(result: Any) -> dict[str, Any]:
    execution = getattr(result, "js_execution_result", None) or {}
    results = execution.get("results") if isinstance(execution, dict) else None
    if not execution.get("success") or not isinstance(results, list) or not results:
        return {"error": execution.get("error") or "JavaScript 抽取没有返回结果", "blocks": []}
    value = results[-1]
    return value if isinstance(value, dict) else {"error": "JavaScript 返回格式错误", "blocks": []}


class FeishuDocCrawler:
    def __init__(self, options: CrawlOptions | None = None):
        self.options = options or CrawlOptions()

    async def crawl(self, source_url: str) -> CrawlArtifacts:
        source_url = validate_source_url(source_url)
        _, chrome_version = detect_chrome_version()
        user_agent = self.options.user_agent or chrome_user_agent(chrome_version)
        api_payloads: dict[str, list[dict[str, Any]]] = {
            "/minutes/doubao/api/subtitles_v2": [],
            "/minutes/doubao/api/speakers": [],
            "/minutes/doubao/api/compose_info": [],
        }
        pending_response_tasks: set[asyncio.Task[Any]] = set()

        async def consume_response(response: Any) -> None:
            parsed = urlsplit(response.url)
            if parsed.path not in api_payloads:
                return
            try:
                payload = json.loads(await response.text())
            except (json.JSONDecodeError, TypeError, ValueError):
                return
            if isinstance(payload, dict):
                api_payloads[parsed.path].append(payload)

        async def on_page_context_created(page: Any, **_: Any) -> Any:
            def schedule_response(response: Any) -> None:
                if urlsplit(response.url).path not in api_payloads:
                    return
                task = asyncio.create_task(consume_response(response))
                pending_response_tasks.add(task)
                task.add_done_callback(pending_response_tasks.discard)

            page.on("response", schedule_response)
            return page

        async def before_return_html(page: Any, **_: Any) -> Any:
            if pending_response_tasks:
                await asyncio.gather(*list(pending_response_tasks), return_exceptions=True)
            return page

        from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

        browser_config = BrowserConfig(
            browser_type="chromium",
            chrome_channel="chrome",
            channel="chrome",
            headless=self.options.headless,
            user_agent=user_agent,
            headers={
                "User-Agent": user_agent,
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            },
            storage_state=(str(self.options.storage_state) if self.options.storage_state else None),
            enable_stealth=True,
            viewport_width=1440,
            viewport_height=1000,
            verbose=False,
        )
        run_config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            wait_until="domcontentloaded",
            page_timeout=self.options.page_timeout_ms,
            delay_before_return_html=self.options.delay_before_extract,
            js_code=DOCUMENT_SCROLL_SCRIPT,
            word_count_threshold=1,
            verbose=False,
        )

        async with AsyncWebCrawler(config=browser_config) as crawler:
            crawler.crawler_strategy.set_hook(
                "on_page_context_created", on_page_context_created
            )
            crawler.crawler_strategy.set_hook("before_return_html", before_return_html)
            result = await crawler.arun(url=source_url, config=run_config)

        document = _js_result(result)
        blocks = parse_document_blocks(document.get("blocks") or [])
        transcript_payload = choose_complete_transcript_payload(
            api_payloads["/minutes/doubao/api/subtitles_v2"]
        )
        valid_speakers_payloads = [
            payload
            for payload in api_payloads["/minutes/doubao/api/speakers"]
            if payload.get("code") == 0 and isinstance(payload.get("data"), dict)
        ]
        speakers_payload = max(
            valid_speakers_payloads,
            key=lambda payload: (
                int(payload["data"].get("has_more") is False),
                len(payload["data"].get("paragraph_to_speaker") or {}),
            ),
            default={},
        )
        compose_payload = next(
            (
                payload
                for payload in reversed(api_payloads["/minutes/doubao/api/compose_info"])
                if payload.get("code") == 0 and isinstance(payload.get("data"), dict)
            ),
            {},
        )
        transcript_paragraphs, transcript_metrics, transcript_errors = parse_transcript(
            transcript_payload, speakers_payload
        )

        errors = list(transcript_errors)
        warnings: list[str] = []
        if not getattr(result, "success", False):
            errors.append(f"Crawl4AI 抓取失败：{getattr(result, 'error_message', '')}")
        if document.get("error"):
            errors.append(str(document["error"]))
        if not document.get("bottom_reached"):
            errors.append("纪要虚拟滚动未稳定到达底部")
        if not blocks:
            errors.append("没有提取到纪要块")
        heading_coverage = document.get("heading_coverage") or {}
        missing_headings = [name for name, present in heading_coverage.items() if not present]
        if missing_headings:
            warnings.append("纪要未发现章节标识：" + ", ".join(missing_headings))
        if transcript_paragraphs and not speakers_payload:
            warnings.append("未获得说话人映射，逐字稿发言人将标记为未知")

        title = str(document.get("title") or "").removesuffix(" - 豆包文档").strip()
        renderable_blocks = [item for item in blocks if is_renderable_document_block(item)]
        compose_basic = (
            compose_payload.get("data", {}).get("basic", {})
            if isinstance(compose_payload.get("data"), dict)
            else {}
        )
        source_duration = parse_number(compose_basic.get("duration"))
        transcript_max_time = parse_number(transcript_metrics.get("max_time"))
        duration_coverage = (
            transcript_max_time / source_duration
            if source_duration and transcript_max_time is not None
            else None
        )
        if duration_coverage is not None and duration_coverage < 0.9:
            warnings.append(
                f"逐字稿末尾时间仅覆盖录音时长的 {duration_coverage:.1%}"
            )
        document_metrics = {
            "bottom_reached": bool(document.get("bottom_reached")),
            "stable_bottom_rounds": document.get("stable_bottom_rounds"),
            "final_scroll_height": document.get("final_scroll_height"),
            "client_height": document.get("client_height"),
            "unique_block_count": len(blocks),
            "nonempty_block_count": sum(bool(item.text) for item in blocks),
            "text_chars": sum(len(item.text) for item in blocks),
            "renderable_block_count": len(renderable_blocks),
            "renderable_text_chars": sum(len(item.text) for item in renderable_blocks),
            "heading_coverage": heading_coverage,
            "scroll_samples": document.get("samples") or [],
            "source_duration": source_duration,
            "transcript_duration_coverage": duration_coverage,
        }
        return CrawlArtifacts(
            source_url=source_url,
            captured_at=datetime.now(timezone.utc).isoformat(),
            user_agent=user_agent,
            title=title,
            status_code=getattr(result, "status_code", None),
            blocks=blocks,
            transcript_paragraphs=transcript_paragraphs,
            transcript_payload=transcript_payload,
            speakers_payload=speakers_payload,
            document_metrics=document_metrics,
            transcript_metrics=transcript_metrics,
            warnings=warnings,
            errors=errors,
        )
