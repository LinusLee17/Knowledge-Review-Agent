# Knowledge-Review-Agent

AI repo for turning lecture PDFs into a durable revision knowledge base for Business Analytics, Machine Learning, Statistics, and Data Science.

## What is tracked

```text
README.md
AGENTS.md
requirements.txt
scripts/
src/knowledge_review_agent/
skills/
docs/
tests/
website/
evaluation/*.py
knowledge_base/*/README.md
```

## What stays local

These paths are generated from lecture PDFs or downstream runs and are ignored by git:

- `data/`
- `evaluation/runs/`
- `evaluation/workflow_test_report.md`
- `knowledge_base/concepts/`
- `knowledge_base/refined/`
- `knowledge_base/graphs/*.json`
- `knowledge_base/graphs/deltas/`

## Pipeline

1. `slide_extractor`
   - PDF to structured lecture Markdown / JSON
   - preserves page-level provenance
   - uses the installed Anthropic PDF Skill through the repo bridge

2. `knowledge_consolidator`
   - merges overlapping concepts across lectures and courses
   - writes canonical concept pages
   - keeps provenance and version history

3. `evaluation + quality_gate`
   - checks merge quality before polish
   - blocks refinement when output is weak

4. `presentation_refinement`
   - Impeccable-backed presentation pass
   - reorders and polishes pages without changing meaning

5. `knowledge_graph_builder`
   - builds incremental node / edge data
   - exports `knowledge_base/graphs/graph.json` for the site

6. `graph_visualization`
   - Cytoscape.js UI over graph JSON
   - search, filters, layouts, detail panel

7. `website`
   - renders refined concept pages and interactive graph views

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export ANTHROPIC_PDF_SKILL_COMMAND='...'
python scripts/check_pdf_tooling.py
```

## Core commands

```bash
python scripts/ingest.py \
  --raw data/raw \
  --processed data/processed \
  --index data/index.json \
  --metadata data/metadata.csv

python scripts/consolidate_knowledge.py \
  --processed data/processed \
  --concepts knowledge_base/concepts

python evaluation/evaluate_consolidation.py \
  --concepts knowledge_base/concepts

python scripts/refine_concepts.py \
  --concepts knowledge_base/concepts \
  --refined knowledge_base/refined

python scripts/build_graph.py \
  --concepts knowledge_base/concepts \
  --graphs knowledge_base/graphs
```

## Website

Serve the repo root and open:

```text
http://127.0.0.1:8000/website/index.html
```

The graph UI reads `knowledge_base/graphs/graph.json` directly. It does not rebuild relationships in the browser.

## Notes

- Raw PDFs stay in `data/raw/` locally.
- Incremental ingestion is hash-driven.
- Presentation refinement stays separate from knowledge generation.
- The repo is designed so generated state can grow without being pushed to GitHub.
