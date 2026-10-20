# Scripts

Utility scripts for setup, validation, and batch runs.

Current use:

- `ingest.py`: hash-driven incremental ingestion
- `filter_concepts.py`: lower-level concept filtering and lecture extraction
- `check_pdf_tooling.py`: bridge/env validation
- `audit_repair_concepts.py`: audit or persist draft-only repairs from processed JSON; no PDF parsing or refined-page writes.
- `refine_concepts.py`: prepare pages only with a passing current evaluation report.

Use `python scripts/ingest.py --course BT2102` when extraction rules change for
one course and its PDFs need a scoped refresh. Unchanged courses remain skipped.

Quality pass:

```bash
python scripts/audit_repair_concepts.py
python scripts/audit_repair_concepts.py --apply
python evaluation/evaluate_consolidation.py --asset-root data/raw
# If blocked, fix inputs or supply valid human dispositions, then evaluate again.
python scripts/refine_concepts.py --evaluation evaluation/runs/gates/<report-id>.json
python scripts/build_graph.py
```

Default exclusions: Auto-ML, IS3103, BT2101, BT3102, BT2102. Audit report writes to `evaluation/runs/concept_quality_audit.json`.

Repair apply uses the persistent record store and retains original draft bytes.
It recovers pending transactions before scanning records, so retired duplicates
cannot be recreated from a stale audit scan. Apply rejects the repository's
published root, directories named `refined`, their descendants, and roots that
contain a `refined` directory. Custom draft roots must remain separate from
published output.
The old `--refined` repair option is removed and fails as a usage error. Auditing
or repairing never creates evaluation approvals. Source/asset/review changes
require new evaluation before refinement. See `evaluation/README.md` for policy,
report identity, and review schema.

## Occurrence-aware audit and repair

Audit reads each lecture JSON once into shared in-memory source index. Display
evidence is ranked as before, but repeated wording retains every source location.
Report `source_coverage` contains full accepted match coverage; display cap does
not remove citations. `source_issues` exposes malformed or unreadable sources.

Repair uses only metadata's contributing lectures and exact stored SHA-256 hashes,
with explicit page support and usable text evidence. Empty/missing scope, changed
hashes or evidence only in another lecture blocks that concept's entire repair,
including section repairs and quality-score changes. Report `repair_blocked` gives
reasons. Valid concepts can still repair when an unrelated source is malformed;
corpus-level source issues remain visible.

Audit/repair returns 1 for affected blocked source scope and 0 for successful
audit/repair; normal quality flags remain report data. Consolidation similarly
returns 1 with structured source issues before new canonical writes when source
preflight fails. Neither command silently treats malformed lectures as deleted.
Repairs remain draft-only and require fresh policy-2 evaluation before refinement.

## Graph export paths

`python3 scripts/build_graph.py --repo-root /path/to/repo --concepts knowledge_base/concepts --refined knowledge_base/refined --site website --graphs knowledge_base/graphs`

Relative paths resolve under repo-root; defaults follow that root. Presentation
requires already refined, matching records: evaluate/refine changed drafts before
rebuilding. Validation failure preserves graph.json and exits 1 with error/issues;
internal topology state may already have advanced. Export never refines/evaluates
content. Identical presentation preserves exact old bytes/mtime/timestamp.
