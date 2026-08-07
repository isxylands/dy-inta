from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from .crawler import CrawlOptions, FeishuDocCrawler
from .output import write_artifacts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="crawler_feishu_doc.sh",
        description="完整抓取飞书豆包智能纪要和原始记录"
    )
    parser.add_argument("url", help="https://feishu.doubao.com/docx/... 文档链接")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path.cwd(),
        help="输出目录，支持绝对或相对路径；默认为当前目录",
    )
    parser.add_argument("--user-agent", help="显式覆盖真实 Chrome User-Agent")
    parser.add_argument(
        "--storage-state", type=Path, help="用户已授权导出的 Playwright storage state"
    )
    parser.add_argument("--headed", action="store_true", help="显示 Chrome 窗口")
    parser.add_argument(
        "--delay", type=float, default=10.0, help="页面加载后开始抽取前的等待秒数"
    )
    return parser


async def run(args: argparse.Namespace) -> int:
    options = CrawlOptions(
        headless=not args.headed,
        delay_before_extract=args.delay,
        user_agent=args.user_agent,
        storage_state=args.storage_state,
    )
    artifacts = await FeishuDocCrawler(options).crawl(args.url)
    manifest = write_artifacts(artifacts, args.output)
    summary = {
        "complete": artifacts.complete,
        "output": str(args.output.expanduser().resolve()),
        "document_blocks": len(artifacts.blocks),
        "transcript_paragraphs": len(artifacts.transcript_paragraphs),
        "errors": artifacts.errors,
        "warnings": artifacts.warnings,
        "files": sorted(manifest),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if artifacts.complete else 2


def main() -> None:
    args = build_parser().parse_args()
    raise SystemExit(asyncio.run(run(args)))
