# Scripts

Utility scripts for setup, validation, and batch runs.

Current use:

- `ingest.py`: hash-driven incremental ingestion
- `filter_concepts.py`: lower-level concept filtering and lecture extraction
- `check_pdf_tooling.py`: bridge/env validation
- `audit_repair_concepts.py`: scan and repair flagged concept pages from existing processed JSON; no PDF parsing.

Use `python scripts/ingest.py --course BT2102` when extraction rules change for
one course and its PDFs need a scoped refresh. Unchanged courses remain skipped.

Quality pass:

```bash
python scripts/audit_repair_concepts.py
python scripts/audit_repair_concepts.py --apply
python scripts/build_graph.py
```

Default exclusions: Auto-ML, IS3103, BT2101, BT3102, BT2102. Audit report writes to `evaluation/runs/concept_quality_audit.json`.
