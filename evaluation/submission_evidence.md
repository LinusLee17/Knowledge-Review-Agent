# Submission Evaluation Evidence

This summary points to existing local evaluation evidence. No new PDF parsing or
evaluation run was performed for submission cleanup.

## Evidence source

- Source report: `evaluation/workflow_test_report.md`
- Scope: three lecture-PDF test inputs covering BT4240, CS3244, and BT4012.
- Evaluation scripts: `evaluate_consolidation.py` and `evaluate_graph.py`.

## Recorded results

- Consolidation concepts: 994
- Multi-course concepts: 17
- Orphan concept directories: 35
- Consolidation heuristic score: 98.96
- Graph nodes: 994
- Graph edges: 0
- Graph integrity score: 55.0
- Representative cross-course concept: `Linear Regression`
- Provenance was preserved in concept metadata for the representative result.

## Known limitations

- Concept candidate extraction is too permissive.
- Some concept labels contain OCR-like noise.
- Relation metadata is empty, so the current graph has no edges.
- Presentation refinement was validated as a semantic-equivalent pass-through,
  not as a complete external skill adapter.

The historical report predates the checked-in presentation bundle. The current
bundle contains 66 concepts and 159 graph connections, verified structurally and
through the local website; no new evaluation score is claimed for that bundle.

## Submission validation run

Commands run after packaging:

```bash
pytest -q
python3 evaluation/evaluate_consolidation.py --concepts knowledge_base/concepts
python3 evaluation/evaluate_graph.py --graphs knowledge_base/graphs
```

Results:

- Tests: 8 passed.
- Consolidation: 66 concepts, 0 duplicate key groups, 0 orphan directories,
  66 concepts with provenance, heuristic merge score 100.0.
- Graph: 66 nodes, 159 edges, 0 unresolved targets, 0 self-loops, 0 isolated
  nodes, integrity score 100.0.
- PDF parsing: not run.

Full historical run artifacts remain local under `evaluation/runs/` and are not
part of the GitHub submission.

## Regression validation (2026-10-20)

Commands run against the working tree after review fixes:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider
node --test tests/js/*.test.mjs
PYTHONDONTWRITEBYTECODE=1 python3 evaluation/evaluate_graph.py --presentation
git diff --check
```

- Python: 289 passed, including repair recovery, published-root rejection,
  source conflicts, reference isolation, placeholders, and asset freshness.
- JavaScript: 62 passed, including concept rendering and graph contract checks.
  The HTTP roundtrip test used a temporary loopback listener.
- Published presentation bundle: schema 1, 66 concepts, 159 edges, valid.
- Browser smoke check: graph search and concept navigation; Linear Regression
  equations, table, and legacy source-link targets; no horizontal overflow at
  a 390-pixel viewport. This is sampled UI verification, not a corpus-wide audit.
- Gate policy: 3. Earlier eligibility reports require reevaluation before any
  new refinement; existing published pages remain available without a rebuild.
- No source PDFs parsed and no production ingestion, consolidation, repair,
  refinement, or graph regeneration performed. No new corpus quality score claimed.
