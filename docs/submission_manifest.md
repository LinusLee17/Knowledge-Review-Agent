# Submission Manifest

## Included in GitHub submission

- `src/`: Python package and domain logic.
- `scripts/`: pipeline and validation utilities used by the repository.
- `tests/`: unit tests and test guidance.
- `evaluation/evaluate_consolidation.py`: consolidation evaluation.
- `evaluation/evaluate_graph.py`: graph evaluation.
- `evaluation/submission_evidence.md`: curated evidence summary.
- `website/`: static concept browser and graph visualization.
- `knowledge_base/refined/`: refined concept Markdown and metadata consumed by the website.
- `knowledge_base/graphs/graph.json`: website graph presentation bundle.
- `knowledge_base/graphs/nodes.json`: graph node data used by the website.
- `knowledge_base/graphs/edges.json`: graph edge data used by the website.
- `README.md`, `docs/`, `requirements.txt`, and project instructions.

## Kept local, omitted from GitHub

- `data/`, including raw PDFs, processed lecture artifacts, and ingestion state.
- `knowledge_base/concepts/`, the draft/canonical build output.
- `knowledge_base/graphs/deltas/`, graph history and incremental state.
- `evaluation/runs/`, historical evaluation run directories.
- caches, `__pycache__/`, `.DS_Store`, and temporary outputs.
- one-off design artifacts and local presentation critiques when not referenced by the submission.

Excluded files stay on disk. Cleanup changes GitHub tracking scope only; they are
not permanent local deletion.
