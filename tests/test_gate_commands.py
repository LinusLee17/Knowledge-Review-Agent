import json
from pathlib import Path
import subprocess
import sys

from gate_fixtures import corpus, approved_report, inventory, edit_metadata

ROOT = Path(__file__).resolve().parents[1]


def command(script, *args):
    return subprocess.run([sys.executable, str(ROOT / script), *map(str, args)], cwd=ROOT, capture_output=True, text=True)


def test_evaluation_and_refinement_cli_status(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    args = ['--concepts', paths.concepts_root, '--processed', paths.processed_root,
            '--reviews', paths.reviews_root, '--reports', tmp_path / 'reports']
    evaluation = command('evaluation/evaluate_consolidation.py', *args)
    assert evaluation.returncode == 0, evaluation.stderr
    result = json.loads(evaluation.stdout)
    assert result['eligibility'] == 'pass'
    refined = tmp_path / 'refined'
    output = command('scripts/refine_concepts.py', '--concepts', paths.concepts_root, '--refined', refined,
                     '--evaluation', result['report'])
    assert output.returncode == 0, output.stderr
    before = inventory(refined)
    assert command('scripts/refine_concepts.py', '--concepts', paths.concepts_root, '--refined', refined).returncode == 2
    edit_metadata(directory, definition='')
    blocked = command('evaluation/evaluate_consolidation.py', *args)
    assert blocked.returncode == 1
    assert json.loads(blocked.stdout)['eligibility'] == 'blocked'
    stale = command('scripts/refine_concepts.py', '--concepts', paths.concepts_root, '--refined', refined,
                    '--evaluation', result['report'])
    assert stale.returncode == 1 and inventory(refined) == before


def test_repair_apply_changes_only_persistent_drafts(tmp_path):
    from knowledge_review_agent.quality_gate import require_eligible_report, GateError
    import pytest
    paths, directory, _ = corpus(tmp_path)
    edit_metadata(directory, unknown={"original": True})
    passing = approved_report(paths, tmp_path)
    refined = tmp_path / 'refined'
    refined.mkdir()
    (refined / 'sentinel').write_text('published bytes must stay unchanged')
    before_refined = inventory(refined)
    args = ['--concepts', paths.concepts_root, '--processed', paths.processed_root,
            '--report', tmp_path / 'audit.json']
    # On old code this stays entirely within the temporary fixture and exposes bypass.
    rejected = command('scripts/audit_repair_concepts.py', *args, '--refined', refined, '--apply')
    assert rejected.returncode == 2
    before_drafts = inventory(paths.concepts_root)
    audit = command('scripts/audit_repair_concepts.py', *args)
    assert audit.returncode == 0, audit.stderr
    assert inventory(paths.concepts_root) == before_drafts
    original_meta = (directory / 'metadata.json').read_bytes()
    original_md = (directory / 'concept.md').read_bytes()
    applied = command('scripts/audit_repair_concepts.py', *args, '--apply')
    assert applied.returncode == 0, applied.stderr
    assert json.loads(applied.stdout)['repaired'] == ['Linear Regression']
    assert inventory(refined) == before_refined
    metadata = json.loads((directory / 'metadata.json').read_bytes())
    assert metadata['version_number'] == 2
    archived = list((tmp_path / '.concepts_history').glob('*/*/records/*'))
    assert any((p / 'metadata.json').read_bytes() == original_meta for p in archived)
    assert any((p / 'concept.md').read_bytes() == original_md for p in archived)
    with pytest.raises(GateError): require_eligible_report(passing, paths.concepts_root)


def test_malformed_metadata_cli_saves_blocked_report(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    (directory / 'metadata.json').write_text('[]')
    before = inventory(paths.concepts_root)
    result = command('evaluation/evaluate_consolidation.py', '--concepts', paths.concepts_root,
                     '--processed', paths.processed_root, '--reviews', paths.reviews_root,
                     '--reports', tmp_path / 'reports')
    assert result.returncode == 1 and not result.stderr
    response = json.loads(result.stdout)
    assert response['eligibility'] == 'blocked'
    assert json.loads(Path(response['report']).read_bytes())['findings']
    assert inventory(paths.concepts_root) == before


import pytest

@pytest.mark.parametrize('damage', ['missing_hash', 'wrong_hash', 'empty_scope', 'wrong_course', 'unsupported', 'unrelated', 'empty_evidence'])
def test_repair_rejects_undeclared_or_changed_sources(tmp_path, damage):
    from hashlib import sha256
    paths, directory, lecture = corpus(tmp_path)
    if damage == 'missing_hash': edit_metadata(directory, source_lecture_hashes={})
    elif damage == 'wrong_hash': edit_metadata(directory, source_lecture_hashes={'C1/L1/lecture.json': '0' * 64})
    elif damage == 'empty_scope': edit_metadata(directory, contributing_lecture_files=[])
    elif damage == 'wrong_course': edit_metadata(directory, contributing_courses=['Other'])
    else:
        source = json.loads(lecture.read_bytes())
        if damage == 'unsupported': source['pages'][0]['concepts'] = [{'concept_name': 'Unrelated'}]
        elif damage == 'empty_evidence': source['pages'][0]['extracted_text'] = ''
        else:
            other = paths.processed_root / 'C1' / 'other' / 'lecture.json'
            other.parent.mkdir()
            other.write_bytes(lecture.read_bytes())
            source['pages'][0]['extracted_text'] = 'Unrelated topic.'
            source['pages'][0]['concepts'] = [{'concept_name': 'Unrelated'}]
        lecture.write_text(json.dumps(source))
        edit_metadata(directory, source_lecture_hashes={'C1/L1/lecture.json': sha256(lecture.read_bytes()).hexdigest()})
    before = inventory(paths.concepts_root)
    report = tmp_path / 'audit.json'
    result = command('scripts/audit_repair_concepts.py', '--concepts', paths.concepts_root,
                     '--processed', paths.processed_root, '--report', report, '--apply')
    assert result.returncode == 1, result.stdout + result.stderr
    assert inventory(paths.concepts_root) == before
    data = json.loads(report.read_bytes())
    assert data['findings'][0]['repair_blocked']
    assert not (tmp_path / '.concepts_history').exists()


def test_explicit_scope_ignores_unrelated_invalid_lecture(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    bad = paths.processed_root / 'bad' / 'lecture.json'
    bad.parent.mkdir()
    bad.write_text('[]')
    report = tmp_path / 'audit.json'
    result = command('scripts/audit_repair_concepts.py', '--concepts', paths.concepts_root,
                     '--processed', paths.processed_root, '--report', report, '--apply')
    assert result.returncode == 0, result.stderr
    data = json.loads(report.read_bytes())
    assert data['source_issues'] and data['repaired'] == ['Linear Regression']
    assert not data['findings'][0]['repair_blocked']


def test_audit_builds_index_once_for_multiple_concepts(tmp_path, monkeypatch, capsys):
    import runpy
    import shutil
    paths, directory, lecture = corpus(tmp_path)
    shutil.copytree(directory, paths.concepts_root / 'Second Record')
    ns = runpy.run_path(str(ROOT / 'scripts/audit_repair_concepts.py'))
    globals_ = ns['main'].__globals__
    loader = globals_['load_source_index']
    calls = []
    def load(root):
        calls.append(root)
        return loader(root)
    monkeypatch.setitem(globals_, 'load_source_index', load)
    read = Path.read_bytes
    reads = []
    def counted(path):
        if path == lecture: reads.append(path)
        return read(path)
    monkeypatch.setattr(Path, 'read_bytes', counted)
    monkeypatch.setattr(sys, 'argv', ['audit', '--concepts', str(paths.concepts_root), '--processed', str(paths.processed_root), '--report', str(tmp_path / 'audit.json')])
    before = inventory(paths.concepts_root)
    assert ns['main']() == 0
    assert len(calls) == 1 and reads == [lecture]
    assert inventory(paths.concepts_root) == before
    data = json.loads((tmp_path / 'audit.json').read_bytes())
    assert len(data['findings']) == 2 and data['findings'][0]['source_coverage']


def test_source_trace_survives_audit_repair_and_gate(tmp_path):
    from hashlib import sha256
    from knowledge_review_agent.consolidation import build_mentions, discover_lecture_artifacts
    from knowledge_review_agent.source_occurrences import load_source_index
    from knowledge_review_agent.quality_gate import capture_gate_snapshot
    paths, directory, lecture = corpus(tmp_path)
    data = json.loads(lecture.read_bytes())
    data['pages'][0]['extracted_text'] *= 1
    data['pages'][0]['extracted_text'] += '\n' + data['pages'][0]['extracted_text']
    lecture.write_text(json.dumps(data))
    edit_metadata(directory, source_lecture_hashes={'C1/L1/lecture.json': sha256(lecture.read_bytes()).hexdigest()})
    unrelated = paths.processed_root / 'C1' / 'other' / 'lecture.json'
    unrelated.parent.mkdir()
    unrelated.write_bytes(lecture.read_bytes())
    index = load_source_index(paths.processed_root)
    known = {o.occurrence_id: o for o in index.occurrences}
    mentions = build_mentions(discover_lecture_artifacts(paths.processed_root)[0])
    assert mentions and all(i in known for m in mentions for i in m.occurrence_ids)
    snapshot = capture_gate_snapshot(paths)
    assert all(i in known for c in snapshot.concepts for i in c.source_occurrence_ids)
    passing = approved_report(paths, tmp_path)
    audit_path = tmp_path / 'audit.json'
    args = ['--concepts', paths.concepts_root, '--processed', paths.processed_root, '--report', audit_path]
    before = inventory(paths.concepts_root)
    assert command('scripts/audit_repair_concepts.py', *args).returncode == 0
    assert inventory(paths.concepts_root) == before
    audit = json.loads(audit_path.read_bytes())
    coverage = audit['findings'][0]['source_coverage']
    assert len(coverage) == 2 and all(o['occurrence_id'] in known for o in coverage)
    assert {o['lecture_file'] for o in coverage} == {'C1/L1/lecture.json'}
    assert command('scripts/audit_repair_concepts.py', *args, '--apply').returncode == 0
    refined = tmp_path / 'refined'
    assert command('scripts/refine_concepts.py', '--concepts', paths.concepts_root, '--refined', refined, '--evaluation', passing).returncode == 1
    evaluation = command('evaluation/evaluate_consolidation.py', '--concepts', paths.concepts_root, '--processed', paths.processed_root,
                         '--reviews', paths.reviews_root, '--reports', tmp_path / 'reports')
    assert evaluation.returncode == 0, evaluation.stderr + evaluation.stdout
    current = json.loads(evaluation.stdout)['report']
    assert json.loads(Path(current).read_bytes())['policy_version'] == '3'
    assert command('scripts/refine_concepts.py', '--concepts', paths.concepts_root, '--refined', refined, '--evaluation', current).returncode == 0
    published = inventory(refined)
    assert command('scripts/refine_concepts.py', '--concepts', paths.concepts_root, '--refined', refined, '--evaluation', current).returncode == 0
    assert inventory(refined) == published
    assert json.loads((directory / 'metadata.json').read_bytes())['contributing_lecture_files'] == ['C1/L1/lecture.json']


def test_consolidation_cli_reports_source_error_without_writes(tmp_path):
    paths, directory, lecture = corpus(tmp_path)
    lecture.write_text('[]')
    before = inventory(paths.concepts_root)
    result = command('scripts/consolidate_knowledge.py', '--processed', paths.processed_root, '--concepts', paths.concepts_root)
    assert result.returncode == 1 and 'Traceback' not in result.stderr
    assert json.loads(result.stderr)['issues']
    assert inventory(paths.concepts_root) == before


@pytest.mark.parametrize('target', ['root', 'nested', 'alias', 'ancestor', 'case_variant'])
def test_repair_cannot_target_published_concepts(tmp_path, target):
    import shutil
    paths, directory, _ = corpus(tmp_path)
    published = tmp_path / ('ReFiNeD' if target == 'case_variant' else 'refined')
    shutil.copytree(paths.concepts_root, published)
    selected = published
    if target == 'nested':
        selected = published / directory.name
    elif target == 'alias':
        selected = tmp_path / 'draft-alias'
        selected.symlink_to(published, target_is_directory=True)
    elif target == 'ancestor':
        selected = tmp_path
    before = inventory(published)
    report = tmp_path.parent / (tmp_path.name + '-audit.json')
    result = command('scripts/audit_repair_concepts.py', '--concepts', selected,
                     '--processed', paths.processed_root, '--report', report, '--apply')
    assert result.returncode == 1, result.stdout + result.stderr
    assert 'draft' in result.stderr.lower() and 'refined' in result.stderr.lower()
    assert inventory(published) == before
    assert not report.exists()
    assert not (tmp_path / '.refined_history').exists()


def test_repair_recovers_before_scanning_retired_duplicates(tmp_path, monkeypatch):
    from dataclasses import replace
    import os
    import shutil
    from knowledge_review_agent import concept_store as store

    paths, directory, _ = corpus(tmp_path)
    primary = paths.concepts_root / 'Z Primary'
    directory.rename(primary)
    duplicate = paths.concepts_root / 'A Duplicate'
    shutil.copytree(primary, duplicate)
    metadata = store.load_concept_metadata(primary / 'metadata.json')
    store.save_concept_metadata(primary / 'metadata.json', replace(metadata, version_number=3))
    page = (primary / 'concept.md').read_text()
    real_replace = os.replace

    def interrupt_retirement(source, destination):
        if Path(source) == duplicate:
            raise OSError('synthetic interruption before duplicate retirement')
        return real_replace(source, destination)

    with monkeypatch.context() as patch:
        patch.setattr(os, 'replace', interrupt_retirement)
        with pytest.raises(OSError, match='synthetic interruption'):
            store.write_concept_record(paths.concepts_root, primary,
                replace(metadata, aliases=['merged-only-alias']), lambda final: page,
                superseded_directories=(duplicate,), reason='duplicate merge')
    journal = next(store.concept_history_root(paths.concepts_root).glob('transactions/*/journal.json'))
    assert json.loads(journal.read_bytes())['state'] == 'published'
    result = command('scripts/audit_repair_concepts.py', '--concepts', paths.concepts_root,
                     '--processed', paths.processed_root, '--report', tmp_path / 'audit.json', '--apply')
    assert result.returncode == 0, result.stdout + result.stderr
    assert not duplicate.exists()
    stored = store.load_concept_metadata(primary / 'metadata.json')
    assert stored.version_number >= 4
    assert 'merged-only-alias' in stored.aliases
    assert json.loads(journal.read_bytes())['state'] == 'committed'
    assert len(list(paths.concepts_root.glob('*/metadata.json'))) == 1
