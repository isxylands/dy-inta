from __future__ import annotations

import unittest

from feishu_doc_crawler.crawler import chrome_user_agent, validate_source_url
from feishu_doc_crawler.parsers import (
    choose_complete_transcript_payload,
    format_timestamp,
    is_renderable_document_block,
    parse_document_blocks,
    parse_transcript,
    render_document_markdown,
)


class AdapterTests(unittest.TestCase):
    def test_validates_source_url(self) -> None:
        url = "https://feishu.doubao.com/docx/Abc123"
        self.assertEqual(validate_source_url(url), url)
        with self.assertRaises(ValueError):
            validate_source_url("https://example.com/docx/Abc123")
        with self.assertRaises(ValueError):
            validate_source_url("http://feishu.doubao.com/docx/Abc123")

    def test_builds_version_matched_chrome_user_agent(self) -> None:
        user_agent = chrome_user_agent("151.0.7922.108")
        self.assertIn("Chrome/151.0.7922.108", user_agent)
        self.assertTrue(user_agent.endswith("Safari/537.36"))

    def test_selects_closed_transcript_page(self) -> None:
        partial = {"code": 0, "data": {"size": 10, "total": 56, "paragraphs": []}}
        complete = {"code": 0, "data": {"size": 56, "total": 56, "paragraphs": []}}
        self.assertIs(choose_complete_transcript_payload([partial, complete]), complete)

    def test_parses_and_validates_transcript(self) -> None:
        payload = {
            "code": 0,
            "msg": "success",
            "data": {
                "size": 1,
                "total": 1,
                "has_more": False,
                "paragraphs": [
                    {
                        "pid": "p1",
                        "speaker_name": "发言人 1",
                        "start_time": "1000",
                        "stop_time": "2500",
                        "sentences": [
                            {
                                "sid": "s1",
                                "contents": [
                                    {"cid": "c1", "content": "测试", "start_time": "1000"},
                                    {"cid": "c2", "content": "内容", "stop_time": "2500"},
                                ],
                            }
                        ],
                    }
                ],
            },
        }
        speakers = {
            "code": 0,
            "data": {
                "paragraph_to_speaker": {"p1": "7"},
                "speaker_info_map": {"7": {"marker": {"m_name": "发言人 7"}}},
            },
        }
        paragraphs, metrics, errors = parse_transcript(payload, speakers)
        self.assertEqual(errors, [])
        self.assertEqual(paragraphs[0].text, "测试内容")
        self.assertEqual(paragraphs[0].speaker, "发言人 7")
        self.assertEqual(metrics["content_chunk_count"], 2)
        self.assertEqual(metrics["text_chars"], 4)
        self.assertFalse(metrics["has_more"])

    def test_document_blocks_are_deduplicated_and_rendered(self) -> None:
        blocks = parse_document_blocks(
            [
                {
                    "block_id": "a",
                    "top": 20,
                    "tag": "P",
                    "class": "block docx-text-block",
                    "text": "短",
                },
                {
                    "block_id": "a",
                    "top": 20,
                    "tag": "P",
                    "class": "block docx-text-block",
                    "text": "较完整内容",
                },
                {
                    "block_id": "h",
                    "top": 0,
                    "tag": "H1",
                    "class": "block docx-heading1-block",
                    "text": "总结",
                },
                {
                    "block_id": "container",
                    "top": -10,
                    "tag": "DIV",
                    "class": "block docx-page-block",
                    "text": "总结较完整内容",
                },
            ]
        )
        self.assertEqual([item.block_id for item in blocks], ["container", "h", "a"])
        self.assertFalse(is_renderable_document_block(blocks[0]))
        markdown = render_document_markdown("标题", blocks)
        self.assertIn("# 标题", markdown)
        self.assertIn("## 总结", markdown)
        self.assertIn("较完整内容", markdown)

    def test_formats_millisecond_timestamp(self) -> None:
        self.assertEqual(format_timestamp(65_000, 120_000), "00:01:05")


if __name__ == "__main__":
    unittest.main()
