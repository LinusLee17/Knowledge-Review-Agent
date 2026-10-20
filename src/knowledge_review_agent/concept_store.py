from __future__ import annotations

import json
from dataclasses import asdict, dataclass, fields, replace
from datetime import datetime, timezone
from pathlib import Path
from hashlib import sha256
import os
import shutil
import tempfile
from typing import Callable

from .models import ConceptMetadata, PersistenceAlternative, PersistenceConflict
from .utils import canonical_concept_name, normalize_concept_key


def concept_directory(concepts_root: Path, concept_name: str) -> Path:
    safe_name = concept_name.strip().replace("/", "-").replace("\\", "-")
    return concepts_root / safe_name


def concept_paths(concepts_root: Path, concept_name: str) -> tuple[Path, Path]:
    directory = concept_directory(concepts_root, concept_name)
    return directory / "concept.md", directory / "metadata.json"


def load_concept_metadata(metadata_path: Path) -> ConceptMetadata | None:
    if not metadata_path.exists():
        return None
    payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    defaults = ConceptMetadata(concept_name="")
    values = {}
    for spec in fields(defaults):
        default = getattr(defaults, spec.name)
        value = payload.get(spec.name, default)
        if spec.name == "persistence_conflicts":
            value = [PersistenceConflict(
                field_name=c["field_name"], selected_value=c["selected_value"],
                alternatives=[PersistenceAlternative(**a) for a in c.get("alternatives", [])],
            ) for c in (value or [])]
        elif isinstance(default, str):
            value = str(value or "")
        elif isinstance(default, int):
            value = int(value if value is not None else default)
        elif isinstance(default, float):
            value = float(value or 0)
        elif isinstance(default, list):
            value = list(value or [])
        elif isinstance(default, dict):
            value = dict(value or {})
        values[spec.name] = value
    return ConceptMetadata(**values)


def normalize_concept_metadata(metadata: ConceptMetadata) -> ConceptMetadata:
    values = {}
    for spec in fields(metadata):
        value = getattr(metadata, spec.name)
        if isinstance(value, list) and spec.name != "persistence_conflicts":
            values[spec.name] = sorted(set(value))
        elif isinstance(value, dict):
            values[spec.name] = dict(sorted(value.items()))
    values["canonical_key"] = metadata.canonical_key or normalize_concept_key(metadata.concept_name)
    return replace(metadata, **values)


def render_concept_metadata(metadata: ConceptMetadata) -> str:
    return json.dumps(asdict(normalize_concept_metadata(metadata)), indent=2, ensure_ascii=True)


def save_concept_metadata(metadata_path: Path, metadata: ConceptMetadata) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    if not metadata.last_updated_timestamp:
        metadata = replace(metadata, last_updated_timestamp=datetime.now(timezone.utc).isoformat())
    metadata_path.write_text(render_concept_metadata(metadata), encoding="utf-8")


def merge_concept_metadata(
    concepts_root: Path, records: list[tuple[Path, ConceptMetadata]],
) -> ConceptMetadata:
    if not records:
        raise ValueError("No concept records to merge")
    ordered = sorted(records, key=lambda r: (
        r[1].version_number, r[1].last_updated_timestamp, str(r[0]),
    ), reverse=True)
    primary = ordered[0][1]
    values = {}
    conflicts: dict[str, list[PersistenceAlternative]] = {}
    selected: dict[str, str] = {}
    for _, metadata in ordered:
        for conflict in metadata.persistence_conflicts:
            conflicts.setdefault(conflict.field_name, []).extend(conflict.alternatives)
            selected.setdefault(conflict.field_name, conflict.selected_value)

    def retain(name: str, chosen: str, alternatives: list[tuple[Path, str]]) -> None:
        selected[name] = chosen
        for directory, value in alternatives:
            if value and value != chosen:
                digest = sha256((directory / "metadata.json").read_bytes()).hexdigest()
                conflicts.setdefault(name, []).append(PersistenceAlternative(
                    directory.resolve().relative_to(concepts_root.resolve()).as_posix(), digest, value,
                ))

    for spec in fields(primary):
        name = spec.name
        if name == "persistence_conflicts":
            continue
        original = getattr(primary, name)
        items = [(d, getattr(m, name)) for d, m in ordered]
        if isinstance(original, list):
            values[name] = sorted({v for _, group in items for v in group})
        elif isinstance(original, dict):
            merged = {}
            for _, mapping in reversed(items):
                merged.update(mapping)
            values[name] = merged
            for key, chosen in merged.items():
                retain(f"{name}.{key}", chosen, [(d, v[key]) for d, v in items if key in v])
        elif isinstance(original, str):
            chosen = next((v for _, v in items if v), original)
            values[name] = chosen
            if name not in {"concept_name", "canonical_key", "graph_node_id", "last_updated_timestamp", "persistence_snapshot_id"}:
                retain(name, chosen, items)
        else:
            values[name] = original
    values["persistence_conflicts"] = [PersistenceConflict(
        name, selected[name], sorted(set(alternatives), key=lambda a: (
            a.source_record, a.record_sha256, a.value, a.snapshot_id,
        )),
    ) for name, alternatives in sorted(conflicts.items()) if alternatives]
    return normalize_concept_metadata(replace(primary, **values))


def load_concept_key(metadata_path: Path) -> str:
    metadata = load_concept_metadata(metadata_path)
    if not metadata:
        return ""
    return metadata.canonical_key or normalize_concept_key(metadata.concept_name)


def concept_display_name_from_key(key: str) -> str:
    return canonical_concept_name(key) or key


@dataclass(frozen=True)
class ConceptWriteResult:
    changed: bool
    metadata: ConceptMetadata
    snapshot_id: str = ""
    retired_directories: tuple[str, ...] = ()


def concept_history_root(concepts_root: Path) -> Path:
    return concepts_root.parent / f".{concepts_root.name}_history"


def _digest(payload: object) -> str:
    return sha256(json.dumps(payload, sort_keys=True, ensure_ascii=True).encode()).hexdigest()


def _safe_path(root: Path, relative: str) -> Path:
    part = Path(relative)
    if not relative or part.is_absolute() or any(p in {"..", "."} for p in relative.split("/")):
        raise ValueError(f"Unsafe relative path: {relative}")
    path = root / part
    cursor = path
    while cursor != root:
        if cursor.is_symlink():
            raise ValueError(f"Symlink not supported: {cursor}")
        cursor = cursor.parent
    if root.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path outside root: {path}")
    return path


def _relative_directory(root: Path, directory: Path) -> str:
    try:
        relative = directory.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"Record outside root: {directory}") from exc
    cursor = directory
    while cursor.resolve() != root.resolve():
        if cursor.is_symlink():
            raise ValueError(f"Symlink not supported: {cursor}")
        cursor = cursor.parent
    _safe_path(root, relative)
    return relative


def _inventory(directory: Path) -> dict[str, str | None]:
    if not directory.is_dir() or directory.is_symlink():
        raise ValueError(f"Missing or symlink record directory: {directory}")
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError(f"Unsupported evidence path: {path}")
        result[path.relative_to(directory).as_posix()] = (
            None if path.is_dir() else sha256(path.read_bytes()).hexdigest()
        )
    return result


def _sync_directory(path: Path) -> None:
    if os.name == "posix":
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def _atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".concept-write-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _sync_directory(path.parent)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _atomic_json(path: Path, payload: dict) -> None:
    _atomic_bytes(path, json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=True).encode())


def _verify_snapshot(history: Path, snapshot: str) -> dict:
    directory = _safe_path(history, snapshot)
    manifest = json.loads(_safe_path(directory, "manifest.json").read_text())
    identity = {"canonical_key": manifest["canonical_key"], "originals": manifest["originals"]}
    if manifest.get("schema_version") != 1 or _digest(identity) != directory.name:
        raise ValueError(f"Snapshot manifest mismatch: {directory}")
    for relative, original in manifest["originals"].items():
        # Validate recorded source paths too, even though archives are addressed by ordinal.
        _safe_path(Path("/source-root"), relative)
        archived = _safe_path(directory, original["archive"])
        if _inventory(archived) != original["inventory"]:
            raise ValueError(f"Snapshot bytes mismatch: {archived}")
    return manifest


def _snapshot_relative(key: str, originals: dict[str, dict]) -> str:
    identity = {"canonical_key": key, "originals": originals}
    key_id = f"{normalize_concept_key(key).replace(' ', '-')[:40]}-{sha256(key.encode()).hexdigest()[:16]}"
    # Canonical text is not trusted as a filesystem name.
    key_id = "".join(c if c.isalnum() or c == "-" else "-" for c in key_id)
    return f"{key_id}/{_digest(identity)}"


def _archive_records(
    history: Path, key: str, originals: dict[str, dict], root: Path,
    reason: str, transaction_id: str,
) -> str:
    identity = {"canonical_key": key, "originals": originals}
    relative = _snapshot_relative(key, originals)
    destination = _safe_path(history, relative)
    if destination.exists():
        _verify_snapshot(history, relative)
        return relative
    history.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".snapshot-", dir=history))
    for source, original in originals.items():
        archived = staging / original["archive"]
        shutil.copytree(_safe_path(root, source), archived)
        if _inventory(archived) != original["inventory"]:
            raise ValueError(f"Source changed during archive: {source}")
        for file in archived.rglob("*"):
            if file.is_file():
                with file.open("rb") as stream:
                    os.fsync(stream.fileno())
        for folder in sorted((p for p in archived.rglob("*") if p.is_dir()), reverse=True):
            _sync_directory(folder)
        _sync_directory(archived)
    _atomic_json(staging / "manifest.json", {"schema_version": 1, **identity,
                 "reason": reason, "transaction_id": transaction_id})
    for folder in sorted((p for p in staging.rglob("*") if p.is_dir()), reverse=True):
        _sync_directory(folder)
    _sync_directory(staging)
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.replace(staging, destination)
    _sync_directory(destination.parent)
    return relative


def _resume_transaction(root: Path, history: Path, transaction: Path, journal: dict) -> None:
    if journal.get("schema_version") != 1 or journal.get("state") not in {"prepared", "published", "committed"}:
        raise ValueError("Invalid transaction schema or state")
    if _digest({**journal, "state": "prepared"}) != transaction.name:
        raise ValueError("Transaction journal identity mismatch")
    target = _safe_path(root, journal["target"])
    snapshot = journal["snapshot"]
    originals = _verify_snapshot(history, snapshot)["originals"] if snapshot else {}
    outputs = journal["outputs"]
    if set(outputs) != {"concept.md", "metadata.json"}:
        raise ValueError("Invalid transaction output files")
    for filename, expected in outputs.items():
        staged = _safe_path(transaction, f"staged/{filename}")
        if sha256(staged.read_bytes()).hexdigest() != expected:
            raise ValueError(f"Corrupt staged output: {staged}")
    superseded = journal["superseded"]
    if len(set(superseded)) != len(superseded) or journal["target"] in superseded:
        raise ValueError("Invalid retirement list")
    if any(name not in originals for name in superseded):
        raise ValueError("Retirement lacks original snapshot")
    # Validate every input before completing even the first live operation.
    for relative, original in originals.items():
        source = _safe_path(root, relative)
        if relative in superseded:
            ordinal = list(sorted(originals)).index(relative)
            retired = _safe_path(transaction, f"retired/{ordinal:04d}")
            if source.exists() == retired.exists():
                raise ValueError(f"Ambiguous retirement state: {source}")
            if _inventory(source if source.exists() else retired) != original["inventory"]:
                raise ValueError(f"Retirement input changed: {source}")
        elif relative == journal["target"]:
            current = _inventory(source)
            for name in set(current) | set(original["inventory"]):
                observed = current.get(name)
                old = original["inventory"].get(name)
                if name in outputs:
                    if name not in current or observed not in {old, outputs[name]}:
                        raise ValueError(f"Live file changed: {source / name}")
                elif name not in current or name not in original["inventory"] or observed != old:
                    raise ValueError(f"Live evidence changed: {source / name}")
        else:
            raise ValueError("Unexpected original record")
    if journal["target"] not in originals and target.exists():
        current = _inventory(target)
        if any(name not in outputs or value != outputs[name] for name, value in current.items()):
            raise ValueError(f"New record path changed: {target}")
    for name, expected in outputs.items():
        path = _safe_path(target, name)
        if not path.exists() or sha256(path.read_bytes()).hexdigest() != expected:
            _atomic_bytes(path, _safe_path(transaction, f"staged/{name}").read_bytes())
    if any(sha256(_safe_path(target, name).read_bytes()).hexdigest() != digest for name, digest in outputs.items()):
        raise ValueError("Published record failed verification")
    journal["state"] = "published"
    _atomic_json(transaction / "journal.json", journal)
    for relative in superseded:
        source = _safe_path(root, relative)
        ordinal = list(sorted(originals)).index(relative)
        retired = _safe_path(transaction, f"retired/{ordinal:04d}")
        if source.exists():
            if _inventory(source) != originals[relative]["inventory"]:
                raise ValueError(f"Retirement input changed: {source}")
            retired.parent.mkdir(parents=True, exist_ok=True)
            os.replace(source, retired)
            _sync_directory(source.parent)
            _sync_directory(retired.parent)
    journal["state"] = "committed"
    _atomic_json(transaction / "journal.json", journal)


def recover_concept_transactions(concepts_root: Path) -> list[str]:
    if concepts_root.is_symlink():
        raise ValueError(f"Symlink not supported: {concepts_root}")
    root = concepts_root.resolve()
    history = concept_history_root(root)
    if history.is_symlink():
        raise ValueError(f"Symlink not supported: {history}")
    recovered = []
    transactions = _safe_path(history, "transactions")
    if not transactions.exists():
        return recovered
    for transaction in sorted(transactions.iterdir()):
        try:
            _safe_path(history, transaction.relative_to(history).as_posix())
            path = _safe_path(transaction, "journal.json")
            if not path.exists():  # Unpublished staging; no live writes were authorized.
                continue
            journal = json.loads(path.read_text())
            if journal.get("state") == "committed":
                continue
            _resume_transaction(root, history, transaction, journal)
            recovered.append(transaction.name)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            raise RuntimeError(f"Concept recovery failed; retained evidence at {transaction}: {exc}") from exc
    return recovered


def write_concept_record(
    concepts_root: Path, directory: Path, metadata: ConceptMetadata,
    render_markdown: Callable[[ConceptMetadata], str], *,
    superseded_directories: tuple[Path, ...] = (), reason: str = "update",
) -> ConceptWriteResult:
    recover_concept_transactions(concepts_root)
    root = concepts_root.resolve()
    relative = _relative_directory(root, directory)
    target = _safe_path(root, relative)
    retired = tuple(_relative_directory(root, p) for p in superseded_directories)
    if relative in retired or len(set(retired)) != len(retired):
        raise ValueError("Invalid duplicate retirement paths")
    paths = [relative, *retired]
    if any(a != b and Path(a) in Path(b).parents for a in paths for b in paths):
        raise ValueError("Nested concept records cannot be retired")
    old = load_concept_metadata(target / "metadata.json")
    candidate = normalize_concept_metadata(replace(metadata,
        version_number=old.version_number if old else 1,
        last_updated_timestamp=old.last_updated_timestamp if old else "",
        persistence_snapshot_id=old.persistence_snapshot_id if old else ""))
    if old and not retired and candidate == normalize_concept_metadata(old) and (target / "concept.md").exists():
        if (target / "concept.md").read_text() == render_markdown(candidate):
            return ConceptWriteResult(False, old)
    originals = {}
    versions = []
    for name in sorted(paths):
        source = _safe_path(root, name)
        if source.exists():
            stored = load_concept_metadata(source / "metadata.json")
            originals[name] = {"archive": f"records/{len(originals):04d}", "inventory": _inventory(source),
                               "version_number": stored.version_number if stored else None}
            if stored:
                versions.append(stored.version_number)
        elif name in retired:
            raise ValueError(f"Missing duplicate record: {source}")
    history = concept_history_root(root)
    snapshot = _snapshot_relative(candidate.canonical_key, originals) if originals else ""
    conflicts = []
    for conflict in candidate.persistence_conflicts:
        alternatives = []
        for alternative in conflict.alternatives:
            original = originals.get(alternative.source_record, {})
            digest = original.get("inventory", {}).get("metadata.json")
            if not alternative.snapshot_id and digest == alternative.record_sha256:
                alternative = replace(alternative, snapshot_id=snapshot)
            alternatives.append(alternative)
        conflicts.append(replace(conflict, alternatives=alternatives))
    final = replace(candidate, version_number=max(versions) + 1 if versions else 1,
                    last_updated_timestamp=datetime.now(timezone.utc).isoformat(), persistence_conflicts=conflicts,
                    persistence_snapshot_id=snapshot)
    output = {"concept.md": render_markdown(final).encode(), "metadata.json": render_concept_metadata(final).encode()}
    journal = {"schema_version": 1, "state": "prepared", "target": relative,
               "snapshot": snapshot, "superseded": list(retired), "reason": reason,
               "outputs": {name: sha256(content).hexdigest() for name, content in output.items()}}
    transaction_id = _digest(journal)
    if originals:
        _archive_records(history, candidate.canonical_key, originals, root, reason, transaction_id)
    transaction = _safe_path(history, f"transactions/{transaction_id}")
    if transaction.exists():
        raise RuntimeError(f"Existing concept transaction; inspect recovery evidence at {transaction}")
    for name, content in output.items():
        _atomic_bytes(transaction / "staged" / name, content)
    _atomic_json(transaction / "journal.json", journal)
    _resume_transaction(root, history, transaction, journal)
    return ConceptWriteResult(True, final, snapshot, retired)
