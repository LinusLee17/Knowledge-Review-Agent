import json
from pathlib import Path
from urllib.parse import unquote
import re

import pytest

from knowledge_review_agent import presentation_refinement as presentation
from knowledge_review_agent.quality_gate import GateError, evaluate_for_refinement, write_evaluation_report
from gate_fixtures import corpus, approved_report, inventory, edit_metadata, DEFINITION


def test_presentation_refinement_reorders_sections_without_changing_content(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    (directory / 'concept.md').write_text(f'# Linear Regression\n\n## Provenance\nC1 L1 page 1.\n\n## Definition\n{DEFINITION}\n\n## Classification\nStatistics\n')
    edit_metadata(directory, unknown={'retained': True})
    report = approved_report(paths, tmp_path)
    refined = tmp_path / 'refined'
    result = presentation.refine_concepts(paths.concepts_root, refined, evaluation_report=report)
    output = refined / directory.name
    text = (output / 'concept.md').read_text()
    assert text.index('## Classification') < text.index('## Definition') < text.index('## Provenance')
    assert (output / 'metadata.json').read_bytes() == (directory / 'metadata.json').read_bytes()
    assert result.created == ['Linear Regression']
    before = inventory(refined)
    result = presentation.refine_concepts(paths.concepts_root, refined, evaluation_report=report)
    assert result.unchanged == ['Linear Regression'] and inventory(refined) == before


@pytest.mark.parametrize('mode', ['batch', 'single'])
@pytest.mark.parametrize('state', ['missing', 'blocked', 'stale'])
def test_all_public_entrypoints_block_without_current_pass(tmp_path, mode, state):
    paths, directory, _ = corpus(tmp_path)
    report = approved_report(paths, tmp_path)
    if state == 'blocked':
        edit_metadata(directory, definition='')
        report = write_evaluation_report(evaluate_for_refinement(paths), tmp_path / 'reports')
    elif state == 'stale': edit_metadata(directory, importance_score=2)
    else: report = None
    refined = tmp_path / 'refined'
    refined.mkdir()
    (refined / 'sentinel').write_text('unchanged')
    before = inventory(refined)
    with pytest.raises(GateError):
        if mode == 'batch': presentation.refine_concepts(paths.concepts_root, refined, evaluation_report=report)
        else: presentation.refine_concept_page(directory, refined, evaluation_report=report)
    assert inventory(refined) == before and list(refined.iterdir()) == [refined / 'sentinel']


def test_approved_refinement_preserves_bytes_and_is_idempotent(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    (directory / 'figure one.bin').write_bytes(b'original evidence')
    with (directory / 'concept.md').open('a') as stream:
        stream.write(f'\n## Definition\n{DEFINITION}\n\n## Mathematical Foundation\n$$y = x + 1$$\n| A | B |\n|---|---|\n| 1 | 2 |\n\n```md\n## Fenced heading\n![not asset](missing.png)\n```\n\n![evidence](<figure one.bin> "caption")\n')
    report = approved_report(paths, tmp_path)
    refined = tmp_path / 'refined'
    result = presentation.refine_concept_page(directory, refined, evaluation_report=report)
    output = refined / directory.name
    text = (output / 'concept.md').read_text()
    assert result.created and text.count('## Definition\n') == 2
    assert '$$y = x + 1$$' in text and '| 1 | 2 |' in text and '## Fenced heading' in text
    link = re.search(r'!\[evidence\]\(([^ ]+) "caption"\)', text)[1]
    assert (output / unquote(link.strip('<>'))).read_bytes() == b'original evidence'
    before = inventory(refined)
    presentation.refine_concepts(paths.concepts_root, refined, evaluation_report=report)
    assert inventory(refined) == before


@pytest.mark.parametrize('damage', ['mutation', 'transformation', 'overlap', 'report_inside', 'output_symlink'])
def test_mutation_during_preparation_blocks_all_publication(tmp_path, monkeypatch, damage):
    paths, directory, lecture = corpus(tmp_path)
    report = approved_report(paths, tmp_path)
    refined = tmp_path / 'refined'
    refined.mkdir()
    (refined / 'sentinel').write_text('keep')
    if damage == 'overlap': refined = paths.concepts_root / 'nested-refined'
    elif damage == 'report_inside':
        copied = refined / report.name
        copied.write_bytes(report.read_bytes())
        report = copied
    elif damage == 'output_symlink':
        outside = tmp_path / 'outside'
        outside.mkdir()
        (refined / directory.name).symlink_to(outside, target_is_directory=True)
    else:
        original = presentation.format_concept_document
        def inject(text):
            result = original(text)
            if damage == 'mutation': lecture.write_text(lecture.read_text() + '\n')
            else: result = result.replace(DEFINITION, 'Invented statement.')
            return result
        monkeypatch.setattr(presentation, 'format_concept_document', inject)
    before = inventory(refined)
    with pytest.raises((GateError, ValueError)):
        presentation.refine_concepts(paths.concepts_root, refined, evaluation_report=report)
    assert inventory(refined) == before


@pytest.mark.parametrize('mode', ['batch', 'single'])
def test_history_output_rejected_without_changes(tmp_path, mode):
    paths, directory, _ = corpus(tmp_path)
    report = approved_report(paths, tmp_path)
    history = tmp_path / '.concepts_history'
    archive = history / directory.name
    archive.mkdir(parents=True)
    (archive / 'concept.md').write_text('retained original')
    before = inventory(history)
    with pytest.raises(GateError, match='overlap'):
        if mode == 'batch':
            presentation.refine_concepts(paths.concepts_root, history, evaluation_report=report)
        else:
            presentation.refine_concept_page(directory, history, evaluation_report=report)
    assert inventory(history) == before


def test_reference_asset_relocated_to_original(tmp_path):
    paths, directory, _ = corpus(tmp_path)
    (directory / 'evidence.bin').write_bytes(b'original evidence')
    with (directory / 'concept.md').open('a') as stream:
        stream.write('\n![evidence][asset]\n[asset]: evidence.bin#page=2 "Caption (detail)"\n')
    report = approved_report(paths, tmp_path)
    refined = tmp_path / 'refined'
    presentation.refine_concepts(paths.concepts_root, refined, evaluation_report=report)
    text = (refined / directory.name / 'concept.md').read_text()
    assert '[asset]: ../../concepts/Linear%20Regression/evidence.bin#page=2 "Caption (detail)"' in text


def test_no_quality_scoring_after_formatting(tmp_path, monkeypatch):
    from knowledge_review_agent import quality_gate as gate
    paths, directory, _ = corpus(tmp_path)
    report = approved_report(paths, tmp_path)
    events = []
    score = gate.evaluate_definition_quality
    formatter = presentation.format_concept_document
    def scoring(metadata):
        events.append('score')
        return score(metadata)
    def formatting(text):
        events.append('format')
        return formatter(text)
    monkeypatch.setattr(gate, 'evaluate_definition_quality', scoring)
    monkeypatch.setattr(presentation, 'format_concept_document', formatting)
    presentation.refine_concepts(paths.concepts_root, tmp_path / 'refined', evaluation_report=report)
    assert 'score' not in events[events.index('format') + 1:]


@pytest.mark.parametrize('kind', ['concept', 'review', 'journal'])
def test_final_dependency_membership_check_blocks_publication(tmp_path, monkeypatch, kind):
    paths, directory, _ = corpus(tmp_path)
    report = approved_report(paths, tmp_path)
    original = presentation.format_concept_document
    refined = tmp_path / 'refined'
    def inject(text):
        if kind == 'concept':
            target = paths.concepts_root / 'new' / 'concept.md'
        elif kind == 'review':
            target = paths.reviews_root / 'new.json'
        else:
            target = tmp_path / '.concepts_history' / 'transactions' / 'new' / 'journal.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('{}')
        return original(text)
    monkeypatch.setattr(presentation, 'format_concept_document', inject)
    with pytest.raises(GateError, match='stale'):
        presentation.refine_concepts(paths.concepts_root, refined, evaluation_report=report)
    assert not refined.exists()


def test_no_source_parsing_after_formatting(tmp_path, monkeypatch):
    from knowledge_review_agent import quality_gate as gate
    paths, _, _ = corpus(tmp_path)
    report = approved_report(paths, tmp_path)
    events = []
    indexer = gate.index_sources
    formatter = presentation.format_concept_document
    def index(sources):
        events.append('source_parse')
        return indexer(sources)
    def format_(text):
        events.append('format')
        return formatter(text)
    monkeypatch.setattr(gate, 'index_sources', index)
    monkeypatch.setattr(presentation, 'format_concept_document', format_)
    presentation.refine_concepts(paths.concepts_root, tmp_path / 'refined', evaluation_report=report)
    assert 'source_parse' not in events[events.index('format') + 1:]
