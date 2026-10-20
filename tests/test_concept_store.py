from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path
import os

import pytest

from knowledge_review_agent import concept_store as store
from knowledge_review_agent.models import ConceptMetadata


def record(root, name, **values):
    directory = root / name
    directory.mkdir(parents=True)
    metadata = ConceptMetadata(concept_name="Custom", canonical_key="custom", **values)
    store.save_concept_metadata(directory / "metadata.json", metadata)
    (directory / "concept.md").write_text(f"# Custom\n\n## Definition\n{name}\n")
    return directory, store.load_concept_metadata(directory / "metadata.json")


def test_merge_preserves_all_metadata_fields(tmp_path):
    old = record(tmp_path, "old", version_number=1, definition="Original", domain="Old domain",
                 applications=["Old use"], mathematical_foundation="x=1", topic="Topic")
    new = record(tmp_path, "new", version_number=2, definition="Preferred", domain="New domain",
                 applications=["New use"], scope_level=5, study_priority=2, confidence_score=.8)
    merged = store.merge_concept_metadata(tmp_path, [old, new])
    assert merged.definition == "Preferred"
    assert merged.topic == "Topic"
    assert merged.domain == "New domain"
    assert merged.applications == ["New use", "Old use"]
    assert merged.mathematical_foundation == "x=1"
    assert (merged.scope_level, merged.study_priority, merged.confidence_score) == (5, 2, .8)
    assert merged.version_number == 2  # Store allocates next committed version.


def test_merge_records_conflicting_text_and_hashes(tmp_path):
    old = record(tmp_path, "old", version_number=1, definition="Original", mathematical_foundation="x=1",
                 source_lecture_hashes={"course/lecture.json": "old"})
    new = record(tmp_path, "new", version_number=2, definition="Preferred", mathematical_foundation="x=2",
                 source_lecture_hashes={"course/lecture.json": "new"})
    merged = store.merge_concept_metadata(tmp_path, [old, new])
    conflicts = {c.field_name: c for c in merged.persistence_conflicts}
    assert set(conflicts) == {"definition", "mathematical_foundation", "source_lecture_hashes.course/lecture.json"}
    alternative = conflicts["definition"].alternatives[0]
    assert alternative.value == "Original"
    assert alternative.source_record == "old"
    assert alternative.record_sha256 == sha256((old[0] / "metadata.json").read_bytes()).hexdigest()
    assert merged.source_lecture_hashes["course/lecture.json"] == "new"
    assert store.merge_concept_metadata(tmp_path, [new, old]) == merged


def test_conflict_metadata_roundtrips_and_old_metadata_loads(tmp_path):
    a = record(tmp_path, "a", definition="A", version_number=1)
    b = record(tmp_path, "b", definition="B", version_number=2)
    merged = store.merge_concept_metadata(tmp_path, [a, b])
    store.save_concept_metadata(tmp_path / "merged.json", merged)
    assert store.load_concept_metadata(tmp_path / "merged.json") == merged
    raw = json.loads((a[0] / "metadata.json").read_text())
    raw.pop("persistence_conflicts", None)
    raw["unknown"] = {"retained": True}
    path = tmp_path / "legacy.json"
    path.write_text(json.dumps(raw))
    before = path.read_bytes()
    assert store.load_concept_metadata(path).persistence_conflicts == []
    assert path.read_bytes() == before


def render(metadata):
    return f"# {metadata.concept_name}\nversion: {metadata.version_number}\ntime: {metadata.last_updated_timestamp}\n{metadata.definition}\n"


def inventory(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def test_record_update_archives_original_bytes(tmp_path):
    root = tmp_path / "concepts"
    directory, old = record(root, "Custom", definition="Old", version_number=4)
    path = directory / "metadata.json"
    raw = json.loads(path.read_text())
    raw["unknown"] = {"source": "verbatim"}
    path.write_text(json.dumps(raw))
    (directory / "figure.bin").write_bytes(b"\x00\xff")
    (directory / "empty").mkdir()
    before = {name: data for name, (data, _) in inventory(directory).items()}
    result = store.write_concept_record(root, directory, replace(old, definition="New"), render)
    assert result.changed and result.metadata.version_number == 5
    history = store.concept_history_root(root)
    snapshots = [p for p in history.rglob("manifest.json")]
    assert len(snapshots) == 1
    manifest = json.loads(snapshots[0].read_text())
    assert manifest["reason"] == "update"
    assert manifest["transaction_id"] == next(history.glob("transactions/*/journal.json")).parent.name
    assert manifest["originals"]["Custom"]["version_number"] == 4
    copies = list(snapshots[0].parent.glob("records/*"))
    assert len(copies) == 1
    assert {name: data for name, (data, _) in inventory(copies[0]).items()} == before
    assert (copies[0] / "empty").is_dir()
    assert (directory / "concept.md").read_text() == render(result.metadata)


def test_new_record_and_noop_are_stable(tmp_path):
    root = tmp_path / "concepts"
    directory = root / "Custom"
    metadata = ConceptMetadata(concept_name="Custom", definition="New", version_number=99)
    first = store.write_concept_record(root, directory, metadata, render)
    assert first.metadata.version_number == 1
    before = inventory(tmp_path)
    second = store.write_concept_record(root, directory, metadata, render)
    assert not second.changed
    assert second.metadata == first.metadata
    assert inventory(tmp_path) == before


def test_duplicate_retirement_keeps_both_original_directories(tmp_path):
    root = tmp_path / "concepts"
    primary, metadata = record(root, "primary", version_number=3)
    other, _ = record(root, "other", version_number=1)
    partial, _ = record(root, "partial", version_number=2)
    (partial / "concept.md").unlink()
    for directory in (primary, other, partial):
        (directory / "same.bin").write_bytes(directory.name.encode())
    result = store.write_concept_record(root, primary, metadata, render,
                                        superseded_directories=(other, partial), reason="duplicate merge")
    assert result.metadata.version_number == 4
    assert not other.exists() and not partial.exists()
    history = store.concept_history_root(root)
    assert {p.read_bytes() for p in history.rglob("same.bin")} == {b"primary", b"other", b"partial"}
    assert store.recover_concept_transactions(root) == []


@pytest.mark.parametrize("phase", ["archive", "between_files", "retirement"])
def test_interrupted_write_recovers_once(tmp_path, monkeypatch, phase):
    root = tmp_path / "concepts"
    primary, metadata = record(root, "primary", definition="Old", version_number=3)
    other, _ = record(root, "other", version_number=1)
    last, _ = record(root, "last", version_number=1)
    before = inventory(root)
    replace_file = os.replace

    def interrupt(src, dst):
        dst = Path(dst)
        if (phase == "archive" and dst.name == "manifest.json"
                or phase == "between_files" and dst == primary / "metadata.json"
                or phase == "retirement" and Path(src) == last):
            raise OSError("injected interruption")
        return replace_file(src, dst)

    with monkeypatch.context() as patch:
        patch.setattr(os, "replace", interrupt)
        with pytest.raises(OSError, match="injected interruption"):
            store.write_concept_record(root, primary, replace(metadata, definition="New"), render,
                                       superseded_directories=(other, last))
    if phase == "archive":
        assert inventory(root) == before
        store.write_concept_record(root, primary, replace(metadata, definition="New"), render,
                                   superseded_directories=(other, last))
    else:
        assert store.recover_concept_transactions(root)
    current = store.load_concept_metadata(primary / "metadata.json")
    assert current.definition == "New" and current.version_number == 4
    assert (primary / "concept.md").read_text() == render(current)
    assert not other.exists() and not last.exists()
    after = inventory(tmp_path)
    assert store.recover_concept_transactions(root) == []
    assert inventory(tmp_path) == after


@pytest.mark.parametrize("damage", ["traversal", "absolute", "staged", "snapshot", "retirement"])
def test_recovery_rejects_unsafe_or_corrupt_state(tmp_path, monkeypatch, damage):
    root = tmp_path / "concepts"
    primary, metadata = record(root, "primary", definition="Old")
    other, _ = record(root, "other")
    real_replace = os.replace

    def interrupt(src, dst):
        if Path(dst) == primary / "metadata.json":
            raise OSError("stop after markdown")
        return real_replace(src, dst)

    with monkeypatch.context() as patch:
        patch.setattr(os, "replace", interrupt)
        with pytest.raises(OSError):
            store.write_concept_record(root, primary, replace(metadata, definition="New"), render,
                                       superseded_directories=(other,))
    history = store.concept_history_root(root)
    journal_path = next(history.glob("transactions/*/journal.json"))
    journal = json.loads(journal_path.read_text())
    if damage in {"traversal", "absolute"}:
        journal["target"] = "../external" if damage == "traversal" else str(tmp_path / "external")
        journal_path.write_text(json.dumps(journal))
    elif damage == "staged":
        (journal_path.parent / "staged" / "metadata.json").write_text("corrupt")
    elif damage == "snapshot":
        next(history.glob("*/*/records/*/metadata.json")).write_text("corrupt")
    else:
        (other / "concept.md").write_text("externally changed")
    before = inventory(tmp_path)
    with pytest.raises(RuntimeError, match="recovery"):
        store.recover_concept_transactions(root)
    assert inventory(tmp_path) == before


def test_reject_symlinked_record(tmp_path):
    root = tmp_path / "concepts"
    root.mkdir()
    outside, metadata = record(tmp_path, "outside")
    alias = root / "alias"
    alias.symlink_to(outside, target_is_directory=True)
    before = inventory(outside)
    with pytest.raises((ValueError, RuntimeError), match="[Ss]ymlink|outside"):
        store.write_concept_record(root, alias, metadata, render)
    assert inventory(outside) == before


def test_record_paths_allow_system_parent_alias(tmp_path):
    # macOS /tmp -> /private/tmp is a valid root spelling, not a symlink record.
    alias_parent = tmp_path / "parent-alias"
    actual_parent = tmp_path / "actual-parent"
    actual_parent.mkdir()
    alias_parent.symlink_to(actual_parent, target_is_directory=True)
    root = alias_parent / "concepts"
    result = store.write_concept_record(root, root / "Custom", ConceptMetadata(concept_name="Custom"), render)
    assert result.changed
    assert (actual_parent / "concepts" / "Custom" / "metadata.json").exists()


def test_recovery_rejects_redirected_new_record_journal(tmp_path, monkeypatch):
    root = tmp_path / "concepts"
    intended = root / "intended"
    real_replace = os.replace
    def interrupt(src, dst):
        if Path(dst) == intended / "concept.md":
            raise OSError("before first live replacement")
        return real_replace(src, dst)
    with monkeypatch.context() as patch:
        patch.setattr(os, "replace", interrupt)
        with pytest.raises(OSError):
            store.write_concept_record(root, intended, ConceptMetadata(concept_name="Custom"), render)
    journal_path = next(store.concept_history_root(root).glob("transactions/*/journal.json"))
    journal = json.loads(journal_path.read_text())
    journal["target"] = "unexpected/path"
    journal_path.write_text(json.dumps(journal))
    before = inventory(tmp_path)
    with pytest.raises(RuntimeError, match="recovery"):
        store.recover_concept_transactions(root)
    assert inventory(tmp_path) == before
    assert not (root / "unexpected").exists()
