from __future__ import annotations

import json
import os
import re
from dataclasses import replace
from hashlib import sha256
from pathlib import Path

import pytest
from urllib.parse import unquote, urlsplit

from knowledge_review_agent.concept_store import load_concept_metadata, save_concept_metadata
from knowledge_review_agent.consolidation import consolidate_concepts, discover_concept_records
from knowledge_review_agent.evaluation import evaluate_consolidation
from knowledge_review_agent.models import ConceptMetadata
from knowledge_review_agent.concept_store import concept_history_root


def _write_lecture_json(
    path: Path,
    *,
    course_id: str,
    course_name: str,
    pdf: str,
    pages: list[dict],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "pdf": pdf,
        "course": {
            "course_id": course_id,
            "course_name": course_name,
            "category": "",
            "semester": "",
            "folder": "",
            "notes": "",
        },
        "title": path.parent.name,
        "page_count": max((page["page_number"] for page in pages), default=0),
        "parser_version": "anthropic-pdf-skill-bridge/1",
        "warnings": [],
        "pages": pages,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True), encoding="utf-8")


def _write_concept_fixture(
    concepts_root: Path,
    *,
    directory_name: str,
    concept_name: str,
    canonical_key: str,
    courses: list[str],
    lectures: list[str],
    hashes: dict[str, str],
    timestamp: str,
    version: int,
) -> Path:
    directory = concepts_root / directory_name
    directory.mkdir(parents=True, exist_ok=True)
    metadata = ConceptMetadata(
        concept_name=concept_name,
        canonical_key=canonical_key,
        contributing_courses=courses,
        contributing_lecture_files=lectures,
        source_lecture_hashes=hashes,
        last_updated_timestamp=timestamp,
        version_number=version,
        graph_node_id=canonical_key.replace(" ", "-"),
    )
    (directory / "concept.md").write_text(f"# {concept_name}\n", encoding="utf-8")
    save_concept_metadata(directory / "metadata.json", metadata)
    return directory


def test_consolidate_concepts_merges_duplicates_and_keeps_provenance(tmp_path: Path) -> None:
    processed_root = tmp_path / "data" / "processed"
    concepts_root = tmp_path / "knowledge_base" / "concepts"
    processed_root.mkdir(parents=True)
    concepts_root.mkdir(parents=True)

    _write_concept_fixture(
        concepts_root,
        directory_name="Decision Tree",
        concept_name="Decision Tree",
        canonical_key="decision tree",
        courses=["CS099"],
        lectures=["old/decision_tree/lecture.json"],
        hashes={"old/decision_tree/lecture.json": "oldhash-a"},
        timestamp="2025-01-01T00:00:00+00:00",
        version=1,
    )
    _write_concept_fixture(
        concepts_root,
        directory_name="Decision Trees",
        concept_name="Decision Trees",
        canonical_key="decision tree",
        courses=["STAT200"],
        lectures=["stats/trees/lecture.json"],
        hashes={"stats/trees/lecture.json": "oldhash-b"},
        timestamp="2025-01-02T00:00:00+00:00",
        version=1,
    )

    _write_lecture_json(
        processed_root / "cs101" / "week1" / "lecture.json",
        course_id="CS101",
        course_name="Intro ML",
        pdf="cs101/week1/lecture1.pdf",
        pages=[
            {
                "page_number": 1,
                "heading": "Decision Trees",
                "extracted_text": "Decision Trees split data.\nLinear Regression fits a line.",
                "tables": [],
                "image_count": 0,
                "concept_candidates": ["Decision Trees", "Linear Regression"],
            }
        ],
    )
    _write_lecture_json(
        processed_root / "stats201" / "week2" / "lecture.json",
        course_id="STAT201",
        course_name="Statistics II",
        pdf="stats201/week2/lecture2.pdf",
        pages=[
            {
                "page_number": 1,
                "heading": "Decision Tree",
                "extracted_text": "Decision Tree nodes split on feature thresholds.",
                "tables": [],
                "image_count": 0,
                "concept_candidates": ["Decision Tree"],
            },
            {
                "page_number": 2,
                "heading": "Linear Regression",
                "extracted_text": "Linear Regression minimizes squared error.",
                "tables": [],
                "image_count": 0,
                "concept_candidates": ["Linear Regression"],
            },
        ],
    )

    report = consolidate_concepts(processed_root=processed_root, concepts_root=concepts_root)
    assert "linear regression" in report.created
    assert "decision tree" in report.updated
    assert report.duplicate_dirs

    records = discover_concept_records(concepts_root)
    grouped: dict[str, list] = {}
    for record in records:
        grouped.setdefault(record.key, []).append(record)

    assert set(grouped) == {"decision tree", "linear regression"}
    assert len(grouped["decision tree"]) == 1

    decision_tree = grouped["decision tree"][0].metadata
    assert set(decision_tree.contributing_courses) == {"CS099", "STAT200", "CS101", "STAT201"}
    assert "cs101/week1/lecture.json" in decision_tree.contributing_lecture_files
    assert "stats201/week2/lecture.json" in decision_tree.contributing_lecture_files

    decision_tree_md = grouped["decision tree"][0].directory / "concept.md"
    markdown = decision_tree_md.read_text(encoding="utf-8")
    assert "Decision Trees" in markdown
    assert "cs101/week1/lecture1.pdf" in markdown
    assert "stats201/week2/lecture2.pdf" in markdown
    assert "old/decision_tree/lecture.json" in markdown

    linear_regression_md = grouped["linear regression"][0].directory / "concept.md"
    linear_markdown = linear_regression_md.read_text(encoding="utf-8")
    assert linear_markdown.index("## Definition") < linear_markdown.index("## Why it Matters")
    assert linear_markdown.index("## Why it Matters") < linear_markdown.index("## Core Intuition")
    assert linear_markdown.index("## Core Intuition") < linear_markdown.index("## How it Works")
    assert "## Mathematical Foundation" in linear_markdown
    assert "## Key Components" in linear_markdown
    assert "## Common Mistakes" in linear_markdown
    assert "## Common Variants" in linear_markdown
    assert "## Connections" in linear_markdown
    assert linear_markdown.rfind("## Slide-derived Evidence") > linear_markdown.rfind("## Further Reading")
    assert linear_markdown.rfind("## Provenance") > linear_markdown.rfind("## Slide-derived Evidence")
    assert linear_markdown.rfind("## Extraction Metadata") > linear_markdown.rfind("## Provenance")

    evaluation = evaluate_consolidation(concepts_root)
    assert evaluation.duplicate_key_groups == 0
    assert evaluation.concepts_with_multi_course_provenance >= 1
    assert evaluation.heuristic_merge_score > 0


def _inventory(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def test_duplicate_merge_preserves_metadata_evidence_and_archives(tmp_path):
    concepts = tmp_path / "concepts"
    for name, version, definition in [("Old", 2, "Old exact definition"), ("Preferred", 4, "Preferred exact definition")]:
        directory = _write_concept_fixture(concepts, directory_name=name, concept_name="Custom Topic",
            canonical_key="custom topic", courses=[name], lectures=[f"{name}/lecture.json"],
            hashes={f"{name}/lecture.json": name}, timestamp="2026-01-01", version=version)
        metadata = load_concept_metadata(directory / "metadata.json")
        save_concept_metadata(directory / "metadata.json", replace(metadata, definition=definition,
            mathematical_foundation=f"x={version}", domain="Data Science", topic="Custom",
            applications=[name], scope_level=5, study_priority=2))
        (directory / "concept.md").write_text(f"# Custom Topic\n\n## Definition\n{definition}\n\n## Slide-derived Evidence\n{name} page 3: exact evidence\n\n## Custom Source Detail\n{name} table\n|a|b|\n|1|2|\n")
        (directory / "same.bin").write_bytes(name.encode())
    _write_lecture_json(tmp_path / "processed" / "course" / "lecture.json", course_id="C", course_name="Course",
        pdf="course/input.pdf", pages=[{"page_number": 3, "concepts": [{"concept_name": "Custom Topic",
        "importance_score": 4, "definition": "Current source definition", "evidence": "Current exact evidence"}]}])
    consolidate_concepts(tmp_path / "processed", concepts)
    records = discover_concept_records(concepts)
    assert len(records) == 1
    result = records[0]
    assert result.metadata.definition == "Preferred exact definition"
    assert result.metadata.mathematical_foundation == "x=4"
    assert result.metadata.version_number == 5
    assert result.metadata.applications == ["Old", "Preferred"]
    assert (result.metadata.scope_level, result.metadata.study_priority) == (5, 2)
    text = (result.directory / "concept.md").read_text()
    for needle in ("Old page 3: exact evidence", "Preferred page 3: exact evidence", "Old table", "Preferred table", "Current exact evidence"):
        assert needle in text
    assert "## Quality Review" in text and "definition" in text
    alternatives = [a for c in result.metadata.persistence_conflicts for a in c.alternatives]
    assert all(a.snapshot_id for a in alternatives if not a.source_record.startswith("lecture:"))
    assert any(a.value == "Current source definition" and a.source_record.startswith("lecture:")
               for a in alternatives)
    history = concept_history_root(concepts)
    assert {p.read_bytes() for p in history.rglob("same.bin")} == {b"Old", b"Preferred"}
    before = _inventory(tmp_path)
    consolidate_concepts(tmp_path / "processed", concepts)
    assert _inventory(tmp_path) == before


def test_no_mentions_preserves_existing_record_exactly(tmp_path):
    concepts = tmp_path / "concepts"
    directory = _write_concept_fixture(concepts, directory_name="Custom", concept_name="Custom",
        canonical_key="custom", courses=["C"], lectures=["absent.json"], hashes={"absent.json": "hash"},
        timestamp="2026-01-01", version=4)
    (directory / "concept.md").write_text("# Custom\n\n## Definition\nManual wording and x=2.\n")
    before = _inventory(concepts)
    report = consolidate_concepts(tmp_path / "processed", concepts)
    assert report.unchanged == ["custom"]
    assert _inventory(concepts) == before
    assert not concept_history_root(concepts).exists()


def test_unchanged_sources_do_not_rewrite_records(tmp_path):
    processed = tmp_path / "processed"
    concepts = tmp_path / "concepts"
    for name in ["Linear Regression", "Probability"]:
        _write_lecture_json(processed / name / "lecture.json", course_id=name, course_name=name,
            pdf=f"{name}/input.pdf", pages=[{"page_number": 1, "heading": name,
            "extracted_text": f"{name} exact source definition.", "concept_candidates": [name]}])
    consolidate_concepts(processed, concepts)
    before = _inventory(tmp_path)
    consolidate_concepts(processed, concepts)
    assert _inventory(tmp_path) == before
    unchanged = _inventory(concepts / "Probability")
    lecture = processed / "Linear Regression" / "lecture.json"
    lecture.write_text(lecture.read_text() + "\n")  # Provenance hash changes, meaning does not.
    consolidate_concepts(processed, concepts)
    assert load_concept_metadata(concepts / "Linear Regression" / "metadata.json").version_number == 2
    assert _inventory(concepts / "Probability") == unchanged
    after = _inventory(tmp_path)
    consolidate_concepts(processed, concepts)
    assert _inventory(tmp_path) == after


def test_recovery_precedes_discovery_and_history_stays_invisible(tmp_path, monkeypatch):
    from knowledge_review_agent.graph_builder import build_knowledge_graph
    from knowledge_review_agent.graph_store import load_graph_nodes
    processed = tmp_path / "processed"
    concepts = tmp_path / "concepts"
    for name in ["A", "B"]:
        _write_concept_fixture(concepts, directory_name=name, concept_name="Probability", canonical_key="probability",
            courses=[name], lectures=[f"{name}.json"], hashes={f"{name}.json": name}, timestamp="2026-01-01", version=3)
    actual_replace = os.replace
    def interrupt(src, dst):
        if Path(dst) == concepts / "B" / "metadata.json":
            raise OSError("interrupted consolidation")
        return actual_replace(src, dst)
    with monkeypatch.context() as patch:
        patch.setattr(os, "replace", interrupt)
        with pytest.raises(OSError, match="interrupted consolidation"):
            consolidate_concepts(processed, concepts)
    consolidate_concepts(processed, concepts)
    records = discover_concept_records(concepts)
    assert len(records) == 1 and records[0].metadata.version_number == 4
    assert evaluate_consolidation(concepts).concept_count == 1
    build_knowledge_graph(concepts, tmp_path / "graphs")
    assert len(load_graph_nodes(tmp_path / "graphs" / "nodes.json")) == 1


def test_retained_asset_links_resolve_to_original_bytes(tmp_path):
    concepts = tmp_path / "concepts"
    for name in ["A", "B"]:
        directory = _write_concept_fixture(concepts, directory_name=name, concept_name="Custom", canonical_key="custom",
            courses=[name], lectures=[f"{name}.json"], hashes={f"{name}.json": name}, timestamp="2026-01-01", version=1)
        (directory / "concept.md").write_text(f"# Custom\n\n## Slide-derived Evidence\n![{name}](same.bin)\n")
        (directory / "same.bin").write_bytes(name.encode())
    consolidate_concepts(tmp_path / "processed", concepts)
    current = discover_concept_records(concepts)[0].directory
    text = (current / "concept.md").read_text()
    links = re.findall(r"!\[([AB])\]\(([^)]+)\)", text)
    assert len(links) == 2
    for label, link in links:
        assert (current / unquote(link)).read_bytes() == label.encode()
    # Retained links must remain valid after another content-changing update.
    _write_lecture_json(tmp_path / "processed" / "course" / "lecture.json", course_id="C", course_name="C",
        pdf="course/input.pdf", pages=[{"page_number": 1, "concepts": [{"concept_name": "Custom",
        "canonical_key": "custom", "importance_score": 4, "evidence": "New source evidence"}]}])
    consolidate_concepts(tmp_path / "processed", concepts)
    text = (current / "concept.md").read_text()
    for label, link in re.findall(r"!\[([AB])\]\(([^)]+)\)", text):
        assert (current / unquote(link)).read_bytes() == label.encode()


def test_markdown_only_canonical_evidence_survives_merge(tmp_path):
    concepts = tmp_path / "concepts"
    for name, equation in [("A", "x=1"), ("B", "x=2")]:
        directory = _write_concept_fixture(concepts, directory_name=name, concept_name="Custom", canonical_key="custom",
            courses=[name], lectures=[f"{name}.json"], hashes={f"{name}.json": name}, timestamp="2026-01-01", version=1)
        (directory / "concept.md").write_text(f"# Custom\n\n## Mathematical Foundation\n{equation}\n\n## How it Works\n{name} exact manual steps\n")
    consolidate_concepts(tmp_path / "processed", concepts)
    current = discover_concept_records(concepts)[0]
    text = (current.directory / "concept.md").read_text()
    for needle in ("x=1", "x=2", "A exact manual steps", "B exact manual steps"):
        assert needle in text


def test_mentions_retain_occurrences_without_changing_selection(tmp_path):
    from source_fixtures import lecture_bytes, example_pages
    from knowledge_review_agent.consolidation import discover_lecture_artifacts, build_mentions
    pages = example_pages()
    pages[0]['concepts'] *= 2
    path = tmp_path / 'C1' / 'lecture.json'
    path.parent.mkdir()
    path.write_bytes(lecture_bytes(pages=pages))
    artifact = discover_lecture_artifacts(tmp_path)[0]
    mentions = build_mentions(artifact)
    assert len(mentions) == 1
    assert len(mentions[0].occurrence_ids) == 2
    ids = {o.occurrence_id for o in artifact.source_index.occurrences if o.kind == 'structured'}
    assert set(mentions[0].occurrence_ids) == ids
    pages[0].pop('concepts')
    path.write_bytes(lecture_bytes(pages=pages))
    assert build_mentions(discover_lecture_artifacts(tmp_path)[0])[0].reason_for_inclusion == 'fallback candidate'


def test_source_validation_precedes_canonical_writes(tmp_path):
    from source_fixtures import lecture_bytes, example_pages
    from knowledge_review_agent.source_occurrences import SourceValidationError
    processed = tmp_path / 'processed'
    processed.mkdir()
    (processed / 'lecture.json').write_bytes(lecture_bytes(pages=example_pages()))
    bad = processed / 'bad' / 'lecture.json'
    bad.parent.mkdir()
    bad.write_text('[]')
    with pytest.raises(SourceValidationError) as exc:
        consolidate_concepts(processed, tmp_path / 'concepts')
    assert exc.value.issues
    assert not (tmp_path / 'concepts').exists()
    assert not (tmp_path / '.concepts_history').exists()


def test_consolidation_loads_shared_lectures_once(tmp_path, monkeypatch):
    from source_fixtures import lecture_bytes, example_pages
    processed = tmp_path / 'processed'
    processed.mkdir()
    path = processed / 'lecture.json'
    path.write_bytes(lecture_bytes(pages=example_pages()))
    reads = []
    original = Path.read_bytes
    def record(p):
        if p == path: reads.append(p)
        return original(p)
    monkeypatch.setattr(Path, 'read_bytes', record)
    result = consolidate_concepts(processed, tmp_path / 'concepts')
    assert result.created == ['linear regression']
    assert reads == [path]


def test_consolidation_keeps_array_order_for_duplicate_selection(tmp_path):
    from source_fixtures import lecture_bytes
    from knowledge_review_agent.consolidation import discover_lecture_artifacts, build_mentions
    items = [{'concept_name': 'Noise', 'importance_score': 1} for _ in range(11)]
    items[2] = {'concept_name': 'Linear Regression', 'importance_score': 5, 'evidence': 'same', 'definition': 'Array first definition'}
    items[10] = {**items[2], 'definition': 'Array later definition'}
    page_two = {'page_number': 2, 'concepts': items}
    page_one = {'page_number': 1, 'concepts': [items[2]]}
    path = tmp_path / 'lecture.json'
    path.write_bytes(lecture_bytes(pages=[page_two, page_one], page_count=2))
    mentions = build_mentions(discover_lecture_artifacts(tmp_path)[0])
    assert [m.page_number for m in mentions] == [2, 1]
    assert mentions[0].definition == 'Array first definition'
    assert len(mentions[0].occurrence_ids) == 2


def test_identityless_lecture_aborts_entire_consolidation(tmp_path):
    from source_fixtures import lecture_bytes, example_pages
    from knowledge_review_agent.source_occurrences import SourceValidationError
    processed = tmp_path / 'processed'
    processed.mkdir()
    (processed / 'lecture.json').write_bytes(lecture_bytes(pages=example_pages()))
    bad = processed / 'bad' / 'lecture.json'
    bad.parent.mkdir()
    bad.write_bytes(lecture_bytes(pages=[{'page_number': 1, 'concepts': [{}]}]))
    with pytest.raises(SourceValidationError): consolidate_concepts(processed, tmp_path / 'concepts')
    assert not (tmp_path / 'concepts').exists()


@pytest.mark.parametrize("field_name,preferred,alternatives", [
    ("definition", "Original exact definition.", ["Revised exact definition.", "Other source definition."]),
    ("mathematical_foundation", "x = 1", ["x = 2", "x = 3"]),
])
def test_changed_source_fields_retain_traceable_conflicts(tmp_path, field_name, preferred, alternatives):
    from knowledge_review_agent.consolidation import build_mentions, discover_lecture_artifacts

    processed = tmp_path / "processed"
    concepts = tmp_path / "concepts"
    lecture = processed / "C1" / "lecture.json"

    def write(values):
        _write_lecture_json(lecture, course_id="C1", course_name="Course", pdf="C1/source.pdf",
            pages=[{"page_number": number, "concepts": [{"concept_name": "Custom Topic",
                "importance_score": 4, field_name: value, "evidence": f"Exact page {number} evidence"}]}
                for number, value in enumerate(values, 1)])

    write([preferred])
    consolidate_concepts(processed, concepts)
    original = discover_concept_records(concepts)[0].metadata
    assert getattr(original, field_name) == preferred

    write(alternatives)
    digest = sha256(lecture.read_bytes()).hexdigest()
    mentions = build_mentions(discover_lecture_artifacts(processed)[0])
    consolidate_concepts(processed, concepts)
    current = discover_concept_records(concepts)[0]
    assert getattr(current.metadata, field_name) == preferred
    assert current.metadata.source_lecture_hashes["C1/lecture.json"] == digest
    conflicts = [c for c in current.metadata.persistence_conflicts if c.field_name == field_name]
    assert len(conflicts) == 1
    assert conflicts[0].selected_value == preferred
    assert {a.value for a in conflicts[0].alternatives} == set(alternatives)
    text = (current.directory / "concept.md").read_text()
    for mention in mentions:
        alternative = next(a for a in conflicts[0].alternatives if a.value == getattr(mention, field_name))
        assert alternative.record_sha256 == digest
        assert "C1/lecture.json" in alternative.source_record
        assert f"page={mention.page_number}" in alternative.source_record
        assert mention.occurrence_ids
        assert all(oid in alternative.source_record and oid in text for oid in mention.occurrence_ids)
    assert "lecture SHA-256" in text
    assert "archive pending" not in text
    before = _inventory(tmp_path)
    consolidate_concepts(processed, concepts)
    assert _inventory(tmp_path) == before

    # A later hash-only update must keep earlier alternatives and their references.
    prior_alternatives = set(conflicts[0].alternatives)
    lecture.write_text(lecture.read_text() + "\n")
    consolidate_concepts(processed, concepts)
    updated = discover_concept_records(concepts)[0].metadata
    conflict = next(c for c in updated.persistence_conflicts if c.field_name == field_name)
    assert prior_alternatives <= set(conflict.alternatives)
    before = _inventory(tmp_path)
    consolidate_concepts(processed, concepts)
    assert _inventory(tmp_path) == before


@pytest.mark.parametrize("definition_section", ["Slide-derived Evidence", "Quality Review"])
def test_retained_reference_figure_links_resolve_to_archived_bytes(tmp_path, definition_section):
    concepts = tmp_path / "concepts"
    for name in ["A", "B"]:
        directory = _write_concept_fixture(concepts, directory_name=name, concept_name="Custom",
            canonical_key="custom", courses=[name], lectures=[f"{name}.json"],
            hashes={f"{name}.json": name}, timestamp="2026-01-01", version=1)
        figures = directory / "figures"
        figures.mkdir()
        (figures / "same (plot).bin").write_bytes(name.encode())
        text = f'# Custom\n\n## Slide-derived Evidence\n![{name}][figure-{name}]\n\n'
        if definition_section != "Slide-derived Evidence":
            text += f"## {definition_section}\n"
        (directory / "concept.md").write_text(
            text + f'[figure-{name}]: <figures/same%20(plot).bin?view=1#detail> "Original {name}"\n')

    def check_links():
        current = discover_concept_records(concepts)[0].directory
        text = (current / "concept.md").read_text()
        links = re.findall(r'^\[figure-([AB])\]: <([^>]+)> "Original [AB]"$', text, re.M)
        assert len(links) == 2
        for label, link in links:
            url = urlsplit(link)
            assert (url.query, url.fragment) == ("view=1", "detail")
            destination = (current / unquote(url.path)).resolve()
            assert destination.is_relative_to(concept_history_root(concepts).resolve())
            assert destination.read_bytes() == label.encode()

    consolidate_concepts(tmp_path / "processed", concepts)
    check_links()
    _write_lecture_json(tmp_path / "processed" / "C1" / "lecture.json", course_id="C1",
        course_name="Course", pdf="C1/source.pdf", pages=[{"page_number": 1,
            "concepts": [{"concept_name": "Custom", "importance_score": 4, "evidence": "New evidence"}]}])
    consolidate_concepts(tmp_path / "processed", concepts)
    check_links()


@pytest.mark.parametrize("definition_section", ["Slide-derived Evidence", "Further Reading", "Quality Review"])
def test_retained_same_reference_labels_keep_distinct_images(tmp_path, definition_section):
    concepts = tmp_path / "concepts"
    processed = tmp_path / "processed"
    code = ('`![inline][figure]` and ``![two ticks][figure]``\n'
            '``before ` tick ![example](code-only.bin) ` after``\n'
            '`multiline code\n![example](code-only.bin)\nend code`\n'
            '```markdown\n# Example heading, not a section\n'
            '![fenced][figure]\n[figure]: code-only.bin\n```\n')
    for name in ["A", "B"]:
        directory = _write_concept_fixture(concepts, directory_name=name, concept_name="Custom",
            canonical_key="custom", courses=[name], lectures=[f"{name}.json"],
            hashes={f"{name}.json": name}, timestamp="2026-01-01", version=1)
        (directory / f"own-{name.lower()}.bin").write_bytes(name.encode())
        definition = f'[FiGuRe]: own-{name.lower()}.bin "Original {name}"\n'
        text = f"# Custom\n\n## Slide-derived Evidence\n![{name}][figure]\n\n{code}"
        if definition_section != "Slide-derived Evidence":
            text += f"\n## {definition_section}\n"
        (directory / "concept.md").write_text(text + "\n" + definition)

    def check_links():
        from knowledge_review_agent.concept_document import _lines

        current = discover_concept_records(concepts)[0].directory
        text = (current / "concept.md").read_text()
        assert text.count(code) == 2
        visible = "".join(line for line, active in _lines(text) if active)
        definitions = {}
        for label, path in re.findall(r'^\[([^\]]+)\]: (\S+) "Original [AB]"$', visible, re.M):
            key = " ".join(label.split()).casefold()
            assert key not in definitions, "Merged page contains colliding reference definitions"
            definitions[key] = path
        images = re.findall(r'!\[([AB])\]\[([^\]]+)\]', visible)
        assert len(images) == 2
        for label, reference in images:
            key = " ".join(reference.split()).casefold()
            assert key in definitions, "Reference definition lost across sections"
            path = (current / unquote(urlsplit(definitions[key]).path)).resolve()
            assert path.is_relative_to(concept_history_root(concepts).resolve())
            assert path.read_bytes() == label.encode()
        return text

    consolidate_concepts(processed, concepts)
    check_links()
    before = _inventory(tmp_path)
    consolidate_concepts(processed, concepts)
    assert _inventory(tmp_path) == before
    lecture = processed / "C1" / "lecture.json"
    _write_lecture_json(lecture, course_id="C1", course_name="Course", pdf="C1/source.pdf",
        pages=[{"page_number": 1, "concepts": [{"concept_name": "Custom", "importance_score": 4,
            "evidence": "New source evidence"}]}])
    consolidate_concepts(processed, concepts)
    stable = check_links()
    lecture.write_text(lecture.read_text() + "\n")
    consolidate_concepts(processed, concepts)
    check_links()
    current = discover_concept_records(concepts)[0].directory
    text = (current / "concept.md").read_text()
    retained = lambda value: re.findall(r'<!-- retained-evidence .*?<!-- /retained-evidence -->', value, re.S)
    assert retained(text) == retained(stable)
    before = _inventory(tmp_path)
    consolidate_concepts(processed, concepts)
    assert _inventory(tmp_path) == before


def test_retained_section_split_ignores_fenced_headings():
    from knowledge_review_agent.consolidation import _page_sections

    code = "```markdown\n## Example heading, not a section\n![example][figure]\n```"
    markdown = f"# Custom\n\n## Slide-derived Evidence\n{code}\n\n## Further Reading\nSource\n"
    assert _page_sections(markdown) == [("Slide-derived Evidence", code), ("Further Reading", "Source")]


def test_reference_namespacing_keeps_code_spans_inside_visible_labels():
    from knowledge_review_agent.consolidation import _isolate_source_references

    originals = {name: f'## Slide-derived Evidence\n![{name} `code`][figure]\n\n'
                      f'[figure]: own-{name.lower()}.bin\n'
                 for name in ["A", "B"]}
    isolated = _isolate_source_references(originals)
    for name, text in isolated.items():
        match = re.search(r'!\[' + name + r' `code`\]\[([^\]]+)\]', text)
        assert match and match[1] != "figure"
        assert f'[{match[1]}]: own-{name.lower()}.bin' in text
