from __future__ import annotations

import re
from typing import Any, Iterable

from .models import DocumentBlock, TranscriptParagraph


def parse_number(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_document_blocks(raw_blocks: Iterable[dict[str, Any]]) -> list[DocumentBlock]:
    by_id: dict[str, DocumentBlock] = {}
    for fallback_order, raw in enumerate(raw_blocks):
        block_id = str(raw.get("block_id") or raw.get("id") or "").strip()
        if not block_id:
            continue
        candidate = DocumentBlock(
            block_id=block_id,
            order=int(raw.get("order", fallback_order)),
            top=parse_number(raw.get("top")) or 0.0,
            tag=str(raw.get("tag") or "DIV").upper(),
            css_class=str(raw.get("css_class") or raw.get("class") or ""),
            text=str(raw.get("text") or "").replace("\u200b", "").strip(),
            outer_html=str(raw.get("outer_html") or ""),
            parent_block_id=(
                str(raw["parent_block_id"]) if raw.get("parent_block_id") else None
            ),
        )
        current = by_id.get(block_id)
        if current is None or len(candidate.text) > len(current.text):
            by_id[block_id] = candidate
    return sorted(by_id.values(), key=lambda item: (item.top, item.order, item.block_id))


def choose_complete_transcript_payload(
    payloads: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    valid: list[tuple[int, int, dict[str, Any]]] = []
    for payload in payloads:
        if payload.get("code") != 0 or not isinstance(payload.get("data"), dict):
            continue
        data = payload["data"]
        size = int(data.get("size") or 0)
        total = int(data.get("total") or 0)
        valid.append((int(size == total and total > 0), size, payload))
    if not valid:
        return {}
    return max(valid, key=lambda item: (item[0], item[1]))[2]


def _first_number(items: Iterable[Any]) -> float | None:
    for value in items:
        parsed = parse_number(value)
        if parsed is not None:
            return parsed
    return None


def _speaker_label(
    paragraph: dict[str, Any], speaker_info: dict[str, Any] | None = None
) -> str:
    speaker_info = speaker_info or {}
    marker = speaker_info.get("marker")
    if isinstance(marker, dict) and marker.get("m_name"):
        return str(marker["m_name"])
    for key in ("user_name", "display_name", "name", "nickname"):
        if speaker_info.get(key):
            return str(speaker_info[key])
    for key in (
        "speaker_name",
        "speaker_user_name",
        "user_name",
        "display_name",
        "speaker",
        "speaker_id",
    ):
        value = paragraph.get(key)
        if isinstance(value, dict):
            for nested_key in ("display_name", "name", "nickname", "id"):
                if value.get(nested_key):
                    return str(value[nested_key])
        elif value not in (None, ""):
            return str(value)
    return "未知说话人"


def parse_transcript(
    payload: dict[str, Any],
    speakers_payload: dict[str, Any] | None = None,
) -> tuple[list[TranscriptParagraph], dict[str, Any], list[str]]:
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        return [], {}, ["未获得有效逐字稿响应"]

    raw_paragraphs = data.get("paragraphs")
    if not isinstance(raw_paragraphs, list):
        return [], {}, ["逐字稿响应缺少 data.paragraphs"]

    paragraphs: list[TranscriptParagraph] = []
    sentence_ids: list[str] = []
    content_ids: list[str] = []
    all_times: list[float] = []
    chunk_count = 0
    sentence_count = 0
    speakers_data = (
        speakers_payload.get("data")
        if isinstance(speakers_payload, dict) and speakers_payload.get("code") == 0
        else {}
    )
    paragraph_to_speaker = (
        speakers_data.get("paragraph_to_speaker")
        if isinstance(speakers_data, dict)
        else {}
    ) or {}
    speaker_info_map = (
        speakers_data.get("speaker_info_map") if isinstance(speakers_data, dict) else {}
    ) or {}

    for index, paragraph in enumerate(raw_paragraphs):
        if not isinstance(paragraph, dict):
            continue
        sentences = paragraph.get("sentences") or []
        paragraph_text: list[str] = []
        paragraph_chunks = 0
        paragraph_sentences = 0
        starts: list[Any] = [paragraph.get("start_time")]
        stops: list[Any] = [paragraph.get("stop_time")]

        for sentence in sentences:
            if not isinstance(sentence, dict):
                continue
            paragraph_sentences += 1
            sentence_count += 1
            if sentence.get("sid"):
                sentence_ids.append(str(sentence["sid"]))
            starts.append(sentence.get("start_time"))
            stops.append(sentence.get("stop_time"))
            contents = sentence.get("contents") or []
            sentence_text: list[str] = []
            for content in contents:
                if not isinstance(content, dict):
                    continue
                paragraph_chunks += 1
                chunk_count += 1
                if content.get("cid"):
                    content_ids.append(str(content["cid"]))
                starts.append(content.get("start_time"))
                stops.append(content.get("stop_time"))
                sentence_text.append(str(content.get("content") or ""))
            paragraph_text.append("".join(sentence_text))

        start = _first_number(starts)
        stop_candidates = [value for value in (parse_number(item) for item in stops) if value is not None]
        stop = max(stop_candidates) if stop_candidates else None
        if start is not None:
            all_times.append(start)
        if stop is not None:
            all_times.append(stop)
        paragraph_id = str(paragraph.get("pid") or f"paragraph-{index + 1}")
        speaker_id = paragraph_to_speaker.get(paragraph_id)
        speaker_info = speaker_info_map.get(str(speaker_id), {}) if speaker_id is not None else {}
        speaker = _speaker_label(paragraph, speaker_info)
        if speaker == "未知说话人" and speaker_id is not None:
            speaker = f"发言人 {speaker_id}"
        paragraphs.append(
            TranscriptParagraph(
                paragraph_id=paragraph_id,
                order=index,
                speaker=speaker,
                start_time=start,
                stop_time=stop,
                text="".join(paragraph_text).strip(),
                sentence_count=paragraph_sentences,
                content_chunk_count=paragraph_chunks,
            )
        )

    size = int(data.get("size") or 0)
    total = int(data.get("total") or 0)
    paragraph_ids = [item.paragraph_id for item in paragraphs]
    duplicate_paragraph_ids = len(paragraph_ids) - len(set(paragraph_ids))
    duplicate_sentence_ids = len(sentence_ids) - len(set(sentence_ids))
    duplicate_content_ids = len(content_ids) - len(set(content_ids))
    unknown_speaker_count = sum(item.speaker == "未知说话人" for item in paragraphs)
    errors: list[str] = []
    if not total:
        errors.append("逐字稿 total 为空或为 0")
    if size != total:
        errors.append(f"逐字稿分页未闭合：size={size}, total={total}")
    if len(paragraphs) != total:
        errors.append(f"逐字稿段落数不匹配：paragraphs={len(paragraphs)}, total={total}")
    if data.get("has_more") is True:
        errors.append("逐字稿响应仍标记 has_more=true")
    if duplicate_paragraph_ids:
        errors.append(f"逐字稿存在 {duplicate_paragraph_ids} 个重复 paragraph id")

    metrics = {
        "api_code": payload.get("code"),
        "size": size,
        "total": total,
        "has_more": data.get("has_more"),
        "paragraph_count": len(paragraphs),
        "sentence_count": sentence_count,
        "content_chunk_count": chunk_count,
        "text_chars": sum(len(item.text) for item in paragraphs),
        "nonempty_paragraph_count": sum(bool(item.text) for item in paragraphs),
        "duplicate_paragraph_ids": duplicate_paragraph_ids,
        "duplicate_sentence_ids": duplicate_sentence_ids,
        "duplicate_content_ids": duplicate_content_ids,
        "speaker_count": len({item.speaker for item in paragraphs}),
        "unknown_speaker_count": unknown_speaker_count,
        "min_time": min(all_times) if all_times else None,
        "max_time": max(all_times) if all_times else None,
    }
    return paragraphs, metrics, errors


def is_renderable_document_block(block: DocumentBlock) -> bool:
    css_class = block.css_class.lower()
    return bool(
        re.search(
            r"docx-(?:heading\d+|text|bullet|ordered|image|whiteboard|divider)-block(?:\s|$)",
            css_class,
        )
    )


def render_document_markdown(title: str, blocks: Iterable[DocumentBlock]) -> str:
    lines = [f"# {title}" if title else "# 飞书智能纪要", ""]
    for block in blocks:
        if not is_renderable_document_block(block):
            continue
        text = re.sub(r"[ \t]+", " ", block.text).strip()
        if not text:
            continue
        css_class = block.css_class.lower()
        heading_match = re.search(r"(?:heading|level)[-_ ]?([1-6])", css_class)
        if block.tag in {f"H{level}" for level in range(1, 7)}:
            level = int(block.tag[1])
            lines.extend([f"{'#' * min(level + 1, 6)} {text}", ""])
        elif heading_match:
            level = min(int(heading_match.group(1)) + 1, 6)
            lines.extend([f"{'#' * level} {text}", ""])
        elif block.tag == "LI" or "list" in css_class or "bullet" in css_class:
            lines.append(f"- {text}")
        else:
            lines.extend([text, ""])
    return "\n".join(lines).rstrip() + "\n"


def _time_to_seconds(value: float | None, observed_max: float | None) -> float | None:
    if value is None:
        return None
    if observed_max is not None and observed_max > 100_000:
        return value / 1000.0
    return value


def format_timestamp(value: float | None, observed_max: float | None) -> str:
    seconds = _time_to_seconds(value, observed_max)
    if seconds is None:
        return "--:--:--"
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def render_transcript_markdown(
    title: str,
    paragraphs: Iterable[TranscriptParagraph],
    observed_max: float | None,
) -> str:
    lines = [f"# {title} - 原始记录" if title else "# 原始记录", ""]
    for paragraph in paragraphs:
        timestamp = format_timestamp(paragraph.start_time, observed_max)
        lines.extend([f"## [{timestamp}] {paragraph.speaker}", "", paragraph.text, ""])
    return "\n".join(lines).rstrip() + "\n"
