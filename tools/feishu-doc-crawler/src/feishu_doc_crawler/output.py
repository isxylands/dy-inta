from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .models import CrawlArtifacts
from .parsers import render_document_markdown, render_transcript_markdown


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_artifacts(artifacts: CrawlArtifacts, output_directory: Path) -> dict[str, Any]:
    output_directory = output_directory.expanduser().resolve()
    files: dict[str, bytes] = {
        "minutes.md": render_document_markdown(artifacts.title, artifacts.blocks).encode(
            "utf-8"
        ),
        "minutes.blocks.json": _json_bytes(
            {
                "source_url": artifacts.source_url,
                "captured_at": artifacts.captured_at,
                "title": artifacts.title,
                "blocks": [item.to_dict() for item in artifacts.blocks],
            }
        ),
        "transcript.md": render_transcript_markdown(
            artifacts.title,
            artifacts.transcript_paragraphs,
            artifacts.transcript_metrics.get("max_time"),
        ).encode("utf-8"),
        "transcript.raw.json": _json_bytes(artifacts.transcript_payload),
        "speakers.raw.json": _json_bytes(artifacts.speakers_payload),
        "report.json": _json_bytes(artifacts.report()),
    }
    manifest = {
        name: {
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        for name, content in files.items()
    }
    files["manifest.json"] = _json_bytes(
        {
            "source_url": artifacts.source_url,
            "captured_at": artifacts.captured_at,
            "files": manifest,
        }
    )
    for name, content in files.items():
        _atomic_write(output_directory / name, content)
    return manifest
