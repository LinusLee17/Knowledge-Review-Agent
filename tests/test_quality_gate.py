from dataclasses import replace
from hashlib import sha256
import json
import shutil

import pytest

from knowledge_review_agent import quality_gate as gate
from knowledge_review_agent.evaluation import evaluate_consolidation
from gate_fixtures import corpus, edit_metadata, inventory, DEFINITION, review, approved_report


def test_valid_source_backed_corpus_has_no_hard_findings(tmp_path):
    paths, directory, lecture = corpus(tmp_path)
    before = inventory(tmp_path)
    snapshot = gate.capture_gate_snapshot(paths)
    assert not gate.evaluate_readiness(snapshot)
    assert snapshot == gate.capture_gate_snapshot(paths)
    assert inventory(tmp_path) == before
    assert snapshot.concepts[0].supported_pages == ({"lecture_file": "C1/L1/lecture.json", "page_number": 1, "course": "C1"},)


@pytest.mark.parametrize("definition", ["TODO: add source definition here", "TBD after source review",
    "Needs review: add source definition here", "Definition missing: add source definition here",
    "Not available: awaiting source definition", "Unknown: awaiting source definition"])
def test_placeholder_definition_with_math_is_hard_blocked(tmp_path, definition):
    paths, directory, _ = corpus(tmp_path)
    edit_metadata(directory, definition=definition, mathematical_foundation="x=1")
    (directory / "concept.md").write_text(
        f"# Linear Regression\n\n## Definition\n{definition}\n\n## Mathematical Foundation\nx=1\n")
    report = gate.evaluate_for_refinement(paths)
    assert report["eligibility"] == "blocked"
    assert any(f["code"] == "missing_definition" and f["severity"] == "hard" for f in report["findings"])


def test_definition_can_discuss_unknowns_or_todo_without_being_placeholder(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    definition = "Unknown parameters are estimated by this statistical model; TODO labels identify pending tasks."
    edit_metadata(directory, definition=definition, mathematical_foundation="x=1")
    (directory / "concept.md").write_text(f"# Linear Regression\n\n## Definition\n{definition}\n")
    assert gate.evaluate_for_refinement(paths)["eligibility"] == "pass"


@pytest.mark.parametrize("label", ["Evidence [source]", r"Evidence \[source\]", r"Evidence [source \] detail]"])
def test_bracket_label_assets_block_when_missing_and_track_freshness(tmp_path, label):
    paths, directory, _ = corpus(tmp_path)
    with (directory / "concept.md").open("a") as stream:
        stream.write(f'\n![{label}](missing.png "Evidence title")\n')
    report = gate.evaluate_for_refinement(paths)
    assert report["eligibility"] == "blocked"
    assert any(f["code"] == "invalid_asset" and f["details"]["destination"] == "missing.png"
               for f in report["findings"])
    asset = directory / "missing.png"
    asset.write_bytes(b"first")
    snapshot = gate.capture_gate_snapshot(paths)
    assert not snapshot.findings
    assert snapshot.manifest["concepts/Linear Regression/missing.png"] == sha256(b"first").hexdigest()
    path = approved_report(paths, tmp_path)
    asset.write_bytes(b"changed")
    changed = gate.capture_gate_snapshot(paths)
    assert changed.fingerprint != snapshot.fingerprint
    assert changed.concepts[0].fingerprint != snapshot.concepts[0].fingerprint
    with pytest.raises(gate.GateError, match="stale"):
        gate.require_eligible_report(path, paths.concepts_root)
    with pytest.raises(gate.GateError, match="stale"):
        gate.assert_gate_snapshot_current(snapshot)


def test_code_span_label_missing_asset_blocks_and_creation_invalidates_snapshot(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    with (directory / "concept.md").open("a") as stream:
        stream.write('\n[Evidence `label`](missing.png)\n')
    snapshot = gate.capture_gate_snapshot(paths)
    assert any(f.code == 'invalid_asset' and f.severity == 'hard' for f in snapshot.findings)
    assert gate.evaluate_for_refinement(paths)['eligibility'] == 'blocked'
    (directory / 'missing.png').write_bytes(b'evidence')
    assert gate.capture_gate_snapshot(paths).fingerprint != snapshot.fingerprint
    with pytest.raises(gate.GateError, match='stale'):
        gate.assert_gate_snapshot_current(snapshot)


def test_code_span_label_asset_enters_manifest_and_report_freshness(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    with (directory / "concept.md").open("a") as stream:
        stream.write('\n[Evidence `[example](ignored.png)`](evidence.png)\n')
    asset = directory / 'evidence.png'
    asset.write_bytes(b'evidence')
    path = approved_report(paths, tmp_path)
    snapshot = gate.capture_gate_snapshot(paths)
    asset.write_bytes(b'changed')
    with pytest.raises(gate.GateError, match='stale'):
        gate.require_eligible_report(path, paths.concepts_root)
    with pytest.raises(gate.GateError, match='stale'):
        gate.assert_gate_snapshot_current(snapshot)
    assert snapshot.manifest['concepts/Linear Regression/evidence.png'] == sha256(b'evidence').hexdigest()
    assert not any(name.endswith('/ignored.png') for name in snapshot.manifest)


@pytest.mark.parametrize("markup", ['[![Evidence](figure.png)](source.bin)',
                                   '![[Evidence](source.bin)](figure.png)'])
@pytest.mark.parametrize("changed_asset", ['figure.png', 'source.bin'])
def test_nested_image_assets_both_enter_manifest_and_freshness(tmp_path, markup, changed_asset):
    paths, directory, _ = corpus(tmp_path)
    with (directory / "concept.md").open("a") as stream:
        stream.write(f'\n{markup}\n')
    for name in ('figure.png', 'source.bin'):
        (directory / name).write_bytes(b'evidence')
    snapshot = gate.capture_gate_snapshot(paths)
    assert not snapshot.findings
    for name in ('figure.png', 'source.bin'):
        assert snapshot.manifest[f'concepts/Linear Regression/{name}'] == sha256(b'evidence').hexdigest()
    path = approved_report(paths, tmp_path)
    (directory / changed_asset).write_bytes(b'changed')
    changed = gate.capture_gate_snapshot(paths)
    assert changed.concepts[0].fingerprint != snapshot.concepts[0].fingerprint
    with pytest.raises(gate.GateError, match='stale'):
        gate.require_eligible_report(path, paths.concepts_root)
    with pytest.raises(gate.GateError, match='stale'):
        gate.assert_gate_snapshot_current(snapshot)


@pytest.mark.parametrize("case", ["empty_definition", "name_definition", "placeholder", "mismatch", "classification",
    "missing_provenance", "missing_hash", "missing_source", "wrong_hash", "unsupported_page", "wrong_course",
    "duplicate", "partial", "nested", "empty", "symlink", "source_symlink"])
def test_hard_failures_cannot_hide_behind_perfect_score(tmp_path, case):
    paths, directory, lecture = corpus(tmp_path)
    if case == "empty_definition":
        edit_metadata(directory, definition="")
        assert evaluate_consolidation(paths.concepts_root).heuristic_merge_score == 100
    elif case == "name_definition": edit_metadata(directory, definition="Linear Regression")
    elif case == "placeholder": edit_metadata(directory, definition="TBD")
    elif case == "mismatch": (directory / "concept.md").write_text("# Linear Regression\n\n## Definition\nDifferent claim.\n")
    elif case == "classification": edit_metadata(directory, domain="")
    elif case == "missing_provenance": edit_metadata(directory, contributing_courses=[])
    elif case == "missing_hash": edit_metadata(directory, source_lecture_hashes={})
    elif case == "missing_source": lecture.unlink()
    elif case == "wrong_hash": lecture.write_text(lecture.read_text() + "\n")
    elif case in {"unsupported_page", "wrong_course"}:
        raw = json.loads(lecture.read_text())
        if case == "unsupported_page": raw["pages"][0]["concepts"] = [{"concept_name": "Unrelated"}]
        else: raw["course"]["course_id"] = "C2"
        lecture.write_text(json.dumps(raw))
        edit_metadata(directory, source_lecture_hashes={"C1/L1/lecture.json": sha256(lecture.read_bytes()).hexdigest()})
    elif case == "duplicate": shutil.copytree(directory, paths.concepts_root / "Duplicate")
    elif case == "partial": (directory / "concept.md").unlink()
    elif case == "nested": shutil.copytree(directory, directory / "Nested")
    elif case == "empty": shutil.rmtree(paths.concepts_root)
    elif case == "symlink": (paths.concepts_root / "alias").symlink_to(directory, target_is_directory=True)
    elif case == "source_symlink":
        outside = tmp_path / "outside.json"
        lecture.rename(outside)
        lecture.symlink_to(outside)
    before = inventory(tmp_path)
    snapshot = gate.capture_gate_snapshot(paths)
    assert any(f.severity == "hard" and f.remediation for f in snapshot.findings)
    assert inventory(tmp_path) == before


def test_conflicts_quality_notes_and_weak_definition_require_review(tmp_path):
    paths, directory, lecture = corpus(tmp_path)
    edit_metadata(directory, persistence_conflicts=[{"field_name": "definition", "selected_value": DEFINITION,
        "alternatives": [{"source_record": "Old", "record_sha256": "a" * 64, "value": "Old value", "snapshot_id": "old/snapshot"}]}])
    with (directory / "concept.md").open("a") as stream: stream.write("\n## Quality Review\nNeed review.\n")
    snapshot = gate.capture_gate_snapshot(paths)
    assert {f.code for f in snapshot.findings} == {"persistence_conflict", "quality_review"}
    assert all(f.severity == "review" and len(f.finding_id) == 64 for f in snapshot.findings)
    edit_metadata(directory, persistence_conflicts=[], definition="A model.")
    (directory / "concept.md").write_text("# Linear Regression\n\n## Definition\nA model.\n")
    assert {f.code for f in gate.capture_gate_snapshot(paths).findings} == {"weak_definition"}


@pytest.mark.parametrize("kind", ["markdown", "metadata", "add", "remove", "rename", "lecture", "asset", "raw_asset", "archive_asset", "review", "journal"])
def test_fingerprints_cover_membership_source_assets_and_pending_journals(tmp_path, kind):
    paths, directory, lecture = corpus(tmp_path)
    asset = directory / "figure.bin"
    asset.write_bytes(b"before")
    with (directory / "concept.md").open("a") as stream: stream.write("\n![figure](figure.bin)\n")
    if kind in {"raw_asset", "archive_asset"}:
        root = tmp_path / ("raw" if kind == "raw_asset" else ".concepts_history")
        root.mkdir()
        asset = root / "source.bin"
        asset.write_bytes(b"before")
        with (directory / "concept.md").open("a") as stream: stream.write(f"\n[original](../../{root.name}/source.bin)\n")
        if kind == "raw_asset": paths = replace(paths, asset_roots=(root,))
    first = gate.capture_gate_snapshot(paths)
    if kind == "markdown": (directory / "concept.md").write_text((directory / "concept.md").read_text() + "\nText change.\n")
    elif kind == "metadata": edit_metadata(directory, importance_score=3)
    elif kind == "add": shutil.copytree(directory, paths.concepts_root / "Added")
    elif kind == "remove": (directory / "concept.md").unlink()
    elif kind == "rename": directory.rename(directory.with_name("Renamed"))
    elif kind == "lecture": lecture.write_text(lecture.read_text() + "\n")
    elif kind in {"asset", "raw_asset", "archive_asset"}: asset.write_bytes(b"after")
    elif kind == "review":
        paths.reviews_root.mkdir()
        (paths.reviews_root / "review.json").write_text("{}")
    else:
        journal = tmp_path / ".concepts_history" / "transactions" / "pending" / "journal.json"
        journal.parent.mkdir(parents=True)
        journal.write_text('{"state": "prepared"}')
    second = gate.capture_gate_snapshot(paths)
    assert first.fingerprint != second.fingerprint or any(f.severity == "hard" for f in second.findings)
    if kind == "journal": assert any(f.code == "pending_persistence" for f in second.findings)


def test_review_resolves_only_exact_current_findings(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    with (directory / "concept.md").open("a") as stream: stream.write("\n## Quality Review\nReview optional details.\n")
    report = gate.evaluate_for_refinement(paths)
    assert report["eligibility"] == "blocked"
    path, payload = review(paths, report)
    accepted = gate.evaluate_for_refinement(paths)
    assert accepted["eligibility"] == "pass"
    assert accepted["findings"][0]["resolved_by"] == [payload["record_id"]]
    review(paths, report, disposition="not_applicable")
    assert gate.evaluate_for_refinement(paths)["eligibility"] == "blocked"  # Contradictory current decisions.


@pytest.mark.parametrize("damage", ["reviewer", "timestamp", "citation", "fingerprint", "finding", "identity", "partial"])
def test_invalid_reviews_cannot_approve(tmp_path, damage):
    paths, directory, _ = corpus(tmp_path)
    with (directory / "concept.md").open("a") as stream: stream.write("\n## Quality Review\nReview me.\n")
    report = gate.evaluate_for_refinement(paths)
    path, payload = review(paths, report)
    if damage == "reviewer": payload["reviewer"] = ""
    elif damage == "timestamp": payload["reviewed_at"] = "nonsense"
    elif damage == "citation": payload["resolutions"][0]["citations"][0]["page_number"] = 99
    elif damage == "fingerprint": payload["concept_fingerprint"] = "a" * 64
    elif damage == "finding": payload["resolutions"][0]["finding_digest"] = "a" * 64
    elif damage == "identity": payload["record_id"] = "a" * 64
    else: payload["resolutions"] = []
    if damage != "identity":
        payload["record_id"] = gate.content_digest({k: v for k, v in payload.items() if k != "record_id"})
        path.unlink()
        path = paths.reviews_root / f"{payload['record_id']}.json"
    path.write_text(json.dumps(payload))
    assert gate.evaluate_for_refinement(paths)["eligibility"] == "blocked"


def test_review_history_does_not_self_invalidate(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    with (directory / "concept.md").open("a") as stream: stream.write("\n## Quality Review\nOptional item.\n")
    old = gate.evaluate_for_refinement(paths)
    review(paths, old)
    assert gate.evaluate_for_refinement(paths)["eligibility"] == "pass"
    with (directory / "concept.md").open("a") as stream: stream.write("More details.\n")
    current = gate.evaluate_for_refinement(paths)
    assert current["eligibility"] == "blocked"
    review(paths, current)
    assert gate.evaluate_for_refinement(paths)["eligibility"] == "pass"
    assert len(list(paths.reviews_root.glob("*.json"))) == 2


def test_pass_and_blocked_reports_are_content_addressed(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    first = gate.evaluate_for_refinement(paths)
    path = gate.write_evaluation_report(first, tmp_path / "reports")
    before = inventory(tmp_path)
    assert gate.write_evaluation_report(first, tmp_path / "reports") == path
    assert inventory(tmp_path) == before
    gate.require_eligible_report(path, paths.concepts_root)
    edit_metadata(directory, definition="")
    blocked = gate.evaluate_for_refinement(paths)
    blocked_path = gate.write_evaluation_report(blocked, tmp_path / "reports")
    assert blocked_path != path
    with pytest.raises(gate.GateError): gate.require_eligible_report(blocked_path, paths.concepts_root)
    path.write_text("corrupt")
    with pytest.raises(gate.GateError): gate.write_evaluation_report(first, tmp_path / "reports")
    assert path.read_text() == "corrupt"


@pytest.mark.parametrize("damage", ["missing", "legacy", "decision", "policy", "schema", "identity", "findings", "roots", "stale"])
def test_report_validation_rejects_stale_tampered_or_legacy_artifacts(tmp_path, damage):
    paths, directory, _ = corpus(tmp_path)
    report = gate.evaluate_for_refinement(paths)
    path = gate.write_evaluation_report(report, tmp_path / "reports")
    if damage == "missing": path.unlink()
    elif damage == "legacy": path.write_text('{"heuristic_merge_score":100}')
    elif damage == "stale": edit_metadata(directory, importance_score=2)
    else:
        if damage == "decision": report["eligibility"] = "blocked"
        elif damage == "policy": report["policy_version"] = "future"
        elif damage == "schema": report["schema_version"] = True
        elif damage == "identity": report["report_id"] = "a" * 64
        elif damage == "findings": report.pop("findings")
        else: report["roots"]["concepts"] = str(tmp_path / "wrong")
        path.write_text(json.dumps(report))
    before = inventory(tmp_path)
    with pytest.raises(gate.GateError): gate.require_eligible_report(path, paths.concepts_root)
    assert inventory(tmp_path) == before


def test_empty_alias_cannot_match_missing_source_identity(tmp_path):
    from hashlib import sha256
    paths, directory, lecture = corpus(tmp_path)
    payload = json.loads(lecture.read_text())
    payload['pages'][0]['concepts'] = [{'concept_name': 'Unrelated Concept'}]
    lecture.write_text(json.dumps(payload))
    edit_metadata(directory, aliases=['-'], source_lecture_hashes={'C1/L1/lecture.json': sha256(lecture.read_bytes()).hexdigest()})
    report = gate.evaluate_for_refinement(paths)
    assert report['eligibility'] == 'blocked'
    assert any(f['code'] == 'invalid_source' for f in report['findings'])


def test_reference_asset_change_invalidates_report(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    asset = directory / 'evidence.bin'
    asset.write_bytes(b'first')
    with (directory / 'concept.md').open('a') as stream:
        stream.write('\n![evidence][asset]\n[asset]: evidence.bin#page=2 "Caption"\n')
    report = approved_report(paths, tmp_path)
    asset.write_bytes(b'changed')
    with pytest.raises(gate.GateError):
        gate.require_eligible_report(report, paths.concepts_root)


@pytest.mark.parametrize('raw', ['[]', '{"importance_score": Infinity}', '{"importance_score": NaN}'])
def test_malformed_metadata_still_writes_blocked_evidence(tmp_path, raw):
    paths, directory, _ = corpus(tmp_path)
    (directory / 'metadata.json').write_text(raw)
    report = gate.evaluate_for_refinement(paths)
    assert report['eligibility'] == 'blocked'
    assert gate.write_evaluation_report(report, tmp_path / 'reports').is_file()


def test_duplicate_review_sections_have_savable_findings(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    with (directory / 'concept.md').open('a') as stream:
        stream.write('\n## Quality Review\nCheck source.\n\n## Quality Review\nCheck source.\n')
    report = gate.evaluate_for_refinement(paths)
    assert report['eligibility'] == 'blocked'
    gate.write_evaluation_report(report, tmp_path / 'reports')


def test_missing_reference_asset_blocks_and_duplicate_review_can_resolve(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    with (directory / 'concept.md').open('a') as stream:
        stream.write('\n![image][asset]\n[asset]: missing.bin\n')
    report = gate.evaluate_for_refinement(paths)
    assert report['eligibility'] == 'blocked'
    assert any(f['code'] == 'invalid_asset' for f in report['findings'])
    (directory / 'missing.bin').write_bytes(b'evidence')
    with (directory / 'concept.md').open('a') as stream:
        stream.write('\n## Quality Review\nCheck source.\n\n## Quality Review\nCheck source.\n')
    report = gate.evaluate_for_refinement(paths)
    gate.write_evaluation_report(report, tmp_path / 'reports')
    review(paths, report)
    passing = gate.evaluate_for_refinement(paths)
    assert passing['eligibility'] == 'pass'
    gate.write_evaluation_report(passing, tmp_path / 'reports')
    assert (directory / 'concept.md').read_text().count('## Quality Review') == 2


@pytest.mark.parametrize('label', ['concept_label', 'name', 'title', 'concept_name'])
def test_gate_shared_identity_and_unique_page_support(tmp_path, label):
    from knowledge_review_agent.source_occurrences import index_sources
    paths, directory, lecture = corpus(tmp_path)
    data = json.loads(lecture.read_bytes())
    data['course'] = {'course_name': 'C1'}
    data['pages'][0]['concepts'] = [{label: 'Linear Regression'}, {label: 'Linear Regression'}]
    lecture.write_text(json.dumps(data))
    edit_metadata(directory, source_lecture_hashes={'C1/L1/lecture.json': sha256(lecture.read_bytes()).hexdigest()})
    snapshot = gate.capture_gate_snapshot(paths)
    assert not snapshot.findings
    concept = snapshot.concepts[0]
    assert len(concept.supported_pages) == 1
    index = index_sources([('C1/L1/lecture.json', lecture.read_bytes())])
    assert set(concept.source_occurrence_ids) == {o.occurrence_id for o in index.find('Linear Regression').occurrences}


@pytest.mark.parametrize('kind', ['explicit_conflict', 'text_only'])
def test_explicit_key_conflict_and_text_only_do_not_pass(tmp_path, kind):
    paths, directory, lecture = corpus(tmp_path)
    data = json.loads(lecture.read_bytes())
    if kind == 'explicit_conflict': data['pages'][0]['concepts'][0]['canonical_key'] = 'unrelated'
    else: data['pages'][0]['concepts'] = []
    lecture.write_text(json.dumps(data))
    edit_metadata(directory, source_lecture_hashes={'C1/L1/lecture.json': sha256(lecture.read_bytes()).hexdigest()})
    report = gate.evaluate_for_refinement(paths)
    assert report['eligibility'] == 'blocked'
    assert gate.write_evaluation_report(report, tmp_path / 'reports').exists()


@pytest.mark.parametrize('policy_version', ['1', '2'])
def test_previous_gate_policy_requires_reevaluation(tmp_path, policy_version):
    paths, _, _ = corpus(tmp_path)
    report = gate.evaluate_for_refinement(paths)
    report['policy_version'] = policy_version
    report['report_id'] = gate.content_digest({k: v for k, v in report.items() if k != 'report_id'})
    output = tmp_path / (report['report_id'] + '.json')
    output.write_text(json.dumps(report))
    with pytest.raises(gate.GateError, match='Unsupported'):
        gate.load_evaluation_report(output)


def test_gate_indexes_captured_sources_once(tmp_path, monkeypatch):
    from knowledge_review_agent.source_occurrences import index_sources
    import shutil
    paths, directory, lecture = corpus(tmp_path)
    # Distinct canonical keys share same source via declared aliases.
    second = paths.concepts_root / 'Second'
    shutil.copytree(directory, second)
    edit_metadata(second, canonical_key='second')
    calls = []
    def capture(sources):
        sources = list(sources)
        calls.append(sources)
        return index_sources(sources)
    monkeypatch.setattr(gate, 'index_sources', capture)
    snapshot = gate.capture_gate_snapshot(paths)
    assert len(calls) == 1 and len(calls[0]) == 1
    assert not snapshot.findings


@pytest.mark.parametrize('damage', ['duplicate_page', 'missing_page', 'bool_page', 'source_pdf', 'source_page', 'nan', 'array'])
def test_gate_persists_blocked_source_issues(tmp_path, damage):
    paths, directory, lecture = corpus(tmp_path)
    data = json.loads(lecture.read_bytes())
    page = data['pages'][0]
    if damage == 'duplicate_page': data['pages'].append(page)
    elif damage == 'missing_page': page.pop('page_number')
    elif damage == 'bool_page': page['page_number'] = True
    elif damage == 'source_pdf': page['concepts'][0]['source'] = {'pdf': 'other.pdf'}
    elif damage == 'source_page': page['concepts'][0]['source'] = {'page': 2}
    elif damage == 'nan': data['extra'] = float('nan')
    elif damage == 'array': data = []
    lecture.write_text(json.dumps(data))
    edit_metadata(directory, source_lecture_hashes={'C1/L1/lecture.json': sha256(lecture.read_bytes()).hexdigest()})
    before = inventory(tmp_path)
    report = gate.evaluate_for_refinement(paths)
    assert report['eligibility'] == 'blocked'
    assert inventory(tmp_path) == before
    assert any(f['code'] == 'invalid_source' for f in report['findings'])
    gate.write_evaluation_report(report, tmp_path / 'reports')
