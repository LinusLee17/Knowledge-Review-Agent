# Scripts

Utility scripts for setup, validation, and batch runs.

Current use:

- `ingest.py`: hash-driven incremental ingestion
- `filter_concepts.py`: lower-level concept filtering and lecture extraction
- `check_pdf_tooling.py`: bridge/env validation

Use `python scripts/ingest.py --course BT2102` when extraction rules change for
one course and its PDFs need a scoped refresh. Unchanged courses remain skipped.
