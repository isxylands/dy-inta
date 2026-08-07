from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class DocumentBlock:
    block_id: str
    order: int
    top: float
    tag: str
    css_class: str
    text: str
    outer_html: str
    parent_block_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TranscriptParagraph:
    paragraph_id: str
    order: int
    speaker: str
    start_time: float | None
    stop_time: float | None
    text: str
    sentence_count: int
    content_chunk_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CrawlArtifacts:
    source_url: str
    captured_at: str
    user_agent: str
    title: str
    status_code: int | None
    blocks: list[DocumentBlock]
    transcript_paragraphs: list[TranscriptParagraph]
    transcript_payload: dict[str, Any]
    speakers_payload: dict[str, Any]
    document_metrics: dict[str, Any]
    transcript_metrics: dict[str, Any]
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def complete(self) -> bool:
        return not self.errors

    def report(self) -> dict[str, Any]:
        return {
            "source_url": self.source_url,
            "captured_at": self.captured_at,
            "user_agent": self.user_agent,
            "title": self.title,
            "status_code": self.status_code,
            "complete": self.complete,
            "document": self.document_metrics,
            "transcript": self.transcript_metrics,
            "warnings": self.warnings,
            "errors": self.errors,
        }
