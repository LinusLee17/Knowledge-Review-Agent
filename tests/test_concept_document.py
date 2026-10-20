import pytest

from knowledge_review_agent import concept_document as document


SOURCE = '''---
concept_name: "Example"
---

# Example

## Applications
First use.

## Definition
Exact definition.

```markdown
# Code title
## Code section
![not an asset](missing.png)
```

## Definition
Second definition.

## Mathematical Foundation
$$x_{t+1} = x_t + 1$$
| A | B |
|---|---|
| 1 | 2 |

## Real-world Applications
Second use.
'''


def test_fences_and_duplicate_sections_preserve_content():
    parsed = document.parse_concept_document(SOURCE)
    assert parsed.title == "Example"
    assert len(parsed.sections) == 5
    result = document.format_concept_document(SOURCE)
    assert result.count("## Definition\n") == 2
    assert "## Code section" in result
    assert "First use." in result and "Second use." in result
    assert result.startswith('---\nconcept_name: "Example"\n---\n')
    document.assert_presentation_preserved(SOURCE, result)
    assert document.format_concept_document(result) == result


def test_local_links_preserve_targets_fragments_and_titles():
    text = SOURCE + '\n![figure](<figure one.png> "Caption")\n[PDF](../raw/source.pdf#page=3)\n[web](https://example.com)\n[here](#definition)\n'
    links = document.local_document_links(text)
    assert set(links) == {"figure one.png", "../raw/source.pdf#page=3"}


@pytest.mark.parametrize("old,new", [("x_t + 1", "x_t + 2"), ("| 1 | 2 |", "| 1 | 3 |"),
                                       ("Second definition.", ""), ("First use.", "New claim.")])
def test_transform_invariant_rejects_changed_claims(old, new):
    with pytest.raises(ValueError, match="preserv"):
        document.assert_presentation_preserved(SOURCE, SOURCE.replace(old, new))


def test_unclosed_fence_rejected():
    with pytest.raises(ValueError, match="fence"):
        document.format_concept_document("# Title\n\n## Definition\n```\nunclosed")


def test_reference_links_and_parenthesized_titles():
    text = '# Example\n![image][asset]\n[asset]: <figure one.bin#page=2> "Caption (detail)"\n![inline](figure.bin "Caption (detail)")\n`[code]: missing.bin`\n'
    assert set(document.local_document_links(text)) == {'figure one.bin#page=2', 'figure.bin'}
    changed = document.map_document_links(text, lambda path: '../' + path)
    assert '[asset]: <../figure one.bin#page=2> "Caption (detail)"' in changed
    assert '![inline](../figure.bin "Caption (detail)")' in changed
    assert '`[code]: missing.bin`' in changed
    assert document.local_document_links('[path](file(one(two)).bin)') == ('file(one(two)).bin',)


@pytest.mark.parametrize("label", ["Evidence [source]", "Evidence [source [page]]",
    r"Evidence \[source\]", r"Evidence [source \] detail]", r"Evidence \\[source]"])
@pytest.mark.parametrize("marker", ["!", ""])
def test_bracket_labels_preserve_text_and_rebase_only_destination(label, marker):
    text = f'{marker}[{label}](<figure one.png#page=2> "Caption (detail)")\n'
    assert document.local_document_links(text) == ("figure one.png#page=2",)
    assert document.map_document_links(text, lambda path: path) == text
    changed = document.map_document_links(text, lambda path: "../" + path)
    assert changed == f'{marker}[{label}](<../figure one.png#page=2> "Caption (detail)")\n'


def test_bracket_links_inside_code_or_escaped_openers_stay_literal():
    text = (r'\[escaped [label]](missing.png)' + '\n'
            '`![Evidence [source]](missing.png)`\n'
            '``![Evidence \\[source\\]](missing.png)``\n'
            '```markdown\n![Evidence [source]](missing.png)\n```\n')
    assert document.local_document_links(text) == ()
    assert document.map_document_links(text, lambda path: "../" + path) == text


@pytest.mark.parametrize("text,expected,targets", [
    ('[![Evidence](figure.png)](source.pdf)',
     '[![Evidence](../figure.png)](../source.pdf)', ('figure.png', 'source.pdf')),
    ('![[Evidence](source.pdf)](figure.png)',
     '![[Evidence](../source.pdf)](../figure.png)', ('source.pdf', 'figure.png')),
    (r'[![Evidence [source \]]](<figure one.png#page=2> "Caption")](source.pdf "Source")',
     r'[![Evidence [source \]]](<../figure one.png#page=2> "Caption")](../source.pdf "Source")',
     ('figure one.png#page=2', 'source.pdf')),
])
def test_nested_image_links_collect_and_rebase_each_destination_once(text, expected, targets):
    assert document.local_document_links(text) == targets
    assert document.map_document_links(text, lambda path: path) == text
    calls = []
    def rebase(path):
        calls.append(path)
        return '../' + path
    assert document.map_document_links(text, rebase) == expected
    assert tuple(calls) == targets
    literal = f'`{text}`'
    assert document.local_document_links(literal) == ()
    assert document.map_document_links(literal, rebase) == literal
    assert tuple(calls) == targets


@pytest.mark.parametrize("label", ['Evidence `label`', 'Evidence ``[label]``',
                                  'Evidence `[example](ignored.png)`'])
@pytest.mark.parametrize("marker", ['', '!'])
def test_code_spans_in_labels_preserve_outer_link_and_ignore_code_links(label, marker):
    text = f'{marker}[{label}](missing.png "Caption") `[code](ignored.png)`'
    assert document.local_document_links(text) == ('missing.png',)
    assert document.map_document_links(text, lambda path: path) == text
    calls = []
    def rebase(path):
        calls.append(path)
        return '../' + path
    assert document.map_document_links(text, rebase) == (
        f'{marker}[{label}](../missing.png "Caption") `[code](ignored.png)`')
    assert calls == ['missing.png']
