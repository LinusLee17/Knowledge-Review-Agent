import json
from hashlib import sha256
from pathlib import Path

import pytest

from source_fixtures import lecture_bytes, example_pages
from knowledge_review_agent.source_occurrences import index_sources, load_source_index


def test_occurrence_identity_and_raw_text():
    raw = lecture_bytes(pages=example_pages())
    index = index_sources([('C1/L1/lecture.json', raw)])
    assert not index.issues
    found = index.find('Linear Regression').occurrences
    assert {o.kind for o in found} == {'structured', 'candidate'}
    assert next(o for o in found if o.kind == 'structured').text == '  x = 1; μ = 2  '
    line = index.find('Linear Regression', kinds=('text_line',), text_search=True).occurrences[0]
    assert line.text.startswith('  Linear Regression')
    assert line.source.payload['pages'][0]['extracted_text'][line.start:line.end] == line.text
    assert line.line_number == 1 and line.start == 0
    assert all(len(o.occurrence_id) == 64 for o in index.occurrences)
    assert index.records[0].sha256 == sha256(raw).hexdigest()
    with pytest.raises(TypeError): index.records[0].payload['course']['course_id'] = 'bad'
    with pytest.raises(TypeError): found[0].item['changed'] = True


def test_order_hash_changes_and_duplicate_locations():
    pages = example_pages()
    pages[0]['concepts'] *= 2
    raw = lecture_bytes(pages=pages)
    a, b = ('a/lecture.json', raw), ('b/lecture.json', raw)
    first = index_sources([a, b])
    assert first == index_sources([b, a])
    assert len({o.occurrence_id for o in first.occurrences}) == len(first.occurrences)
    assert len(index_sources([a, a]).records) == 1
    conflict = index_sources([a, (a[0], raw + b' ')])
    assert not conflict.records and conflict.issues[0].code == 'duplicate_source'
    assert {o.occurrence_id for o in first.occurrences}.isdisjoint(
        {o.occurrence_id for o in index_sources([(a[0], raw + b' ')]).occurrences})


@pytest.mark.parametrize('field', ['concept_name', 'concept_label', 'name', 'title'])
def test_explicit_keys_aliases_and_text_search(field):
    pages = [{'page_number': 1, 'concepts': [{field: 'Linear Regression', 'canonical_key': 'unrelated'}],
              'extracted_text': 'Linear Regression is explained here.'}]
    index = index_sources([('a.json', lecture_bytes(pages=pages))])
    assert not index.find('Linear Regression', ['-']).occurrences
    assert index.find('Unrelated').occurrences
    pages[0]['concepts'][0].pop('canonical_key')
    pages[0]['concepts'][0]['aliases'] = ['OLS']
    index = index_sources([('a.json', lecture_bytes(pages=pages))])
    assert index.find('OLS').occurrences
    assert not index.find('-').occurrences
    assert index.find('Regression', kinds=('text_line',), text_search=True).occurrences
    with pytest.raises(ValueError): index.find('Regression', text_search=True)


@pytest.mark.parametrize('damage', ['array', 'nan', 'duplicate_key', 'count', 'bool', 'string', 'missing',
    'range', 'duplicate_page', 'course', 'concepts', 'aliases', 'item_source', 'source_page', 'source_pdf', 'candidates'])
def test_invalid_source_is_reportable(damage):
    payload = json.loads(lecture_bytes(pages=example_pages()))
    page = payload['pages'][0]
    if damage == 'array': raw = b'[]'
    elif damage == 'nan': raw = b'{"x":NaN}'
    elif damage == 'duplicate_key': raw = b'{"pages":[],"pages":[]}'
    else:
        if damage == 'count': payload['page_count'] = 0
        elif damage == 'bool': page['page_number'] = True
        elif damage == 'string': page['page_number'] = '1'
        elif damage == 'missing': page.pop('page_number')
        elif damage == 'range': page['page_number'] = 2
        elif damage == 'duplicate_page': payload['pages'].append(dict(page))
        elif damage == 'course': payload['course'] = []
        elif damage == 'concepts': page['concepts'] = [None]
        elif damage == 'aliases': page['concepts'][0]['aliases'] = 'OLS'
        elif damage == 'item_source': page['concepts'][0]['source'] = []
        elif damage == 'source_page': page['concepts'][0]['source'] = {'page': 2}
        elif damage == 'source_pdf': page['concepts'][0]['source'] = {'pdf': 'other.pdf'}
        elif damage == 'candidates': page['concept_candidates'] = 'Linear Regression'
        raw = json.dumps(payload).encode()
    index = index_sources([('a.json', raw)])
    assert index.issues and not index.records and not index.occurrences
    json.dumps([vars(i) for i in index.issues])


def test_scope_is_explicit():
    raw = lecture_bytes(pages=example_pages(), course_id='', course_name='Stats', page_count=2)
    index = index_sources([('a.json', raw), ('bad.json', b'[]')])
    assert index.find('Linear Regression', lecture_hashes={}).issues[0].code == 'missing_source_scope'
    for scope, code in [({'missing.json': sha256(raw).hexdigest()}, 'missing_source'),
                        ({'a.json': 'bad'}, 'invalid_source_hash'),
                        ({'a.json': '0'*64}, 'source_hash_mismatch')]:
        assert index.find('Linear Regression', lecture_hashes=scope).issues[0].code == code
    scope = {'a.json': sha256(raw).hexdigest()}
    assert index.find('Linear Regression', lecture_hashes=scope, allowed_courses={'C1'}).issues[0].code == 'source_course_mismatch'
    match = index.find('Linear Regression', lecture_hashes=scope, allowed_courses={'Stats'})
    assert match.occurrences and not match.issues
    assert index.find('Linear Regression').issues


def test_loader_reads_exact_bytes_once_and_rejects_symlinks(tmp_path, monkeypatch):
    path = tmp_path / 'a' / 'lecture.json'
    path.parent.mkdir()
    raw = lecture_bytes(pages=example_pages())
    path.write_bytes(raw)
    read = Path.read_bytes
    counts = []
    def counted(p):
        counts.append(p)
        return read(p)
    monkeypatch.setattr(Path, 'read_bytes', counted)
    index = load_source_index(tmp_path)
    assert counts == [path] and index.records[0].raw == raw
    (tmp_path / 'alias').symlink_to(path.parent, target_is_directory=True)
    assert load_source_index(tmp_path).issues
    assert load_source_index(tmp_path / 'alias').issues
    assert not load_source_index(tmp_path / 'absent').records
    assert index_sources([('../bad.json', raw)]).issues
    assert index_sources([('/bad.json', raw)]).issues


@pytest.mark.parametrize('item', [{'concepts': [{}]}, {'concepts': [{'concept_name': '---'}]}, {'concept_candidates': ['---']}])
def test_identityless_entries_are_source_issues(item):
    raw = lecture_bytes(pages=[{'page_number': 1, **item}])
    index = index_sources([('bad.json', raw)])
    assert index.issues and not index.records and not index.occurrences
