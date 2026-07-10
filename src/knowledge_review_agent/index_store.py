from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .models import RepositoryIndex, RepositoryIndexEntry


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def load_index(index_path: Path) -> RepositoryIndex:
    if not index_path.exists():
        return RepositoryIndex()

    payload = json.loads(index_path.read_text(encoding="utf-8"))
    entries = [RepositoryIndexEntry(**entry) for entry in payload.get("entries", [])]
    return RepositoryIndex(
        schema_version=int(payload.get("schema_version", 1) or 1),
        parser_version=str(payload.get("parser_version", "") or ""),
        generated_at=str(payload.get("generated_at", "") or ""),
        entries=entries,
    )


def save_index(index: RepositoryIndex, index_path: Path) -> None:
    index.generated_at = datetime.now(timezone.utc).isoformat()
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(
        json.dumps(asdict(index), indent=2, ensure_ascii=True),
        encoding="utf-8",
    )


def index_entries_by_path(index: RepositoryIndex) -> dict[str, RepositoryIndexEntry]:
    return {entry.relative_file_path: entry for entry in index.entries}


def index_entries_by_hash(index: RepositoryIndex) -> dict[str, RepositoryIndexEntry]:
    return {entry.sha256: entry for entry in index.entries}
