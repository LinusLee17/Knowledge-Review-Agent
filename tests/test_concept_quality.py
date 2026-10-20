import json
from pathlib import Path
import pytest

from knowledge_review_agent import concept_quality as quality
from knowledge_review_agent.source_occurrences import index_sources, SourceValidationError
from source_fixtures import lecture_bytes

TEXT = 'Linear Regression is a statistical model relating several input variables to a numeric response.'


def test_grouped_evidence_preserves_all_locations():
    raw = lecture_bytes(pages=[{'page_number': 1, 'extracted_text': TEXT}])
    other = lecture_bytes(pages=[{'page_number': 1, 'extracted_text': TEXT + ' Further details.'}])
    index = index_sources([('a.json', raw), ('b.json', raw), ('c.json', other)])
    selected = quality.select_source_evidence(index, 'Linear Regression', [], {'C1'}, limit=1)
    assert len(selected.evidence) == 1 and len(selected.coverage) == 3
    assert len(selected.evidence[0].occurrences) == 2
    assert {o.source.relative_path for o in selected.evidence[0].occurrences} == {'a.json', 'b.json'}
    assert not quality.select_source_evidence(index, 'Linear Regression', [], {'C1'}, limit=0).evidence
    with pytest.raises(ValueError): quality.select_source_evidence(index, 'Linear Regression', [], {'C1'}, limit=-1)
    finding = quality.audit_definition('Linear Regression', {}, '# Linear Regression\n## Definition\nshort\n', list(selected.evidence))
    data = json.loads(json.dumps(finding.to_dict()))
    assert len(data['evidence'][0]['occurrences']) == 2
    assert 'raw' not in data['evidence'][0]['occurrences'][0]


def test_compatibility_collector_reuses_index(tmp_path, monkeypatch):
    index = index_sources([('a.json', lecture_bytes(pages=[{'page_number': 1, 'extracted_text': TEXT}]))])
    def no_reads(p): raise AssertionError('index should be reused')
    monkeypatch.setattr(Path, 'read_bytes', no_reads)
    found = quality.collect_source_evidence(tmp_path, 'Linear Regression', [], {'C1'}, source_index=index)
    assert found[0].text == TEXT and found[0].lecture_file == 'a.json'
    bad = index_sources([('bad.json', b'[]')])
    with pytest.raises(SourceValidationError):
        quality.collect_source_evidence(tmp_path, 'Linear Regression', [], {'C1'}, source_index=bad)
