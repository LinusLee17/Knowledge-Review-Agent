# Tests

Run from repository root with the installed pytest environment:

```bash
pytest -q -p no:cacheprovider
```

Initial focus:

- provenance checks
- source-to-note mapping
- concept merge rules
- graph edge generation
- lossless duplicate metadata and evidence preservation
- immutable original snapshots, including unknown JSON keys and binary files
- interrupted-write and duplicate-retirement recovery
- rejection of unsafe journals and corrupt recovery evidence
- unchanged-run stability and archive isolation from active concept scans
- exact-input publication gates through CLI and both Python entry points
- source/page/course/hash validation and human review identity/freshness
- duplicate sections, fenced headings, equations, tables, and local asset links
- draft-only repair behavior and unchanged output on gate/preparation failure

Persistence checks use synthetic records under pytest temporary directories:

```bash
pytest tests/test_concept_store.py tests/test_consolidation.py -q
```

Failure injection targets real filesystem operations. These checks do not parse
PDFs, consolidate the local corpus, refine pages, or regenerate published graph
artifacts. Store writes assume a local filesystem with a single writer. A
two-file record is recoverable after interruption, not atomically visible as a
pair during replacement.

Source occurrence tests use synthetic lecture JSON only: exact wording/locators,
stable identities, immutable values, source validation, explicit hash scope,
read-once index reuse, grouped citation coverage, declared-source repair blocking,
cross-consumer lineage and absence of source parsing after presentation starts.
No production corpus or PDF parser runs during these checks.

Graph presentation: `pytest -q -p no:cacheprovider` and
`node --test tests/js/*.test.mjs`. Shared v1/v2 fixtures pin Python/JS
validation, exact URLs, calendar/rounding, graph topology and statistics. Tests use
synthetic records, read-only shipped v1 compatibility and temporary loopback HTTP
server (requires sandbox permission to listen locally). No production rebuild.

Concept renderer regressions cover fenced headings, introductory prose, images,
relative assets, source links with parentheses, and unsafe URL schemes. They use
the same pure Markdown module consumed by the browser and a temporary viewer
fixture; no source PDFs or published pages are changed.
