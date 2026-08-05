# Knowledge-Review-Agent

Agent for turning scattered lecture notes into a one stop revision knowledge base.

## Pipeline

1. `concept_filter`
   - Extracts durable concepts from parsed lecture content
   - Filters slide noise
   - Assigns domains and topics to concepts

2. `knowledge_consolidator`
   - Merges overlapping concepts across lectures and courses
   - Writes canonical concept pages
   - Synthesizes one explanation
   - Preserves source material and references

3. `evaluation + quality_gate`
   - LLM-as-a-judge to evaluate completeness, factual accuracy, hallucination risk, clarity, usefulness for revision / interview preparation.
   - Checks merge quality before polish
   - Blocks refinement when output is weak

4. `presentation_refinement`
   - Impeccable-backed presentation pass
   - Reorders and polishes pages without changing meaning

5. `knowledge_graph_builder`
   - Normalizes relationships between concepts
   - Connects prerequisites and related concepts
   - Builds incremental node / edge data
   - Exports `knowledge_base/graphs/graph.json` for the site

6. `graph_visualization`
   - Cytoscape.js UI over graph JSON
   - Search, filters, layouts, detail panel

7. `website`
   - renders refined concept pages and interactive graph views

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export ANTHROPIC_PDF_SKILL_COMMAND="/Users/linus/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/linus/Downloads/Knowledge-Review-Agent/scripts/pdf_skill_bridge.py"
python scripts/check_pdf_tooling.py
```

## Core commands

```bash
python scripts/ingest.py \
  --raw data/raw \
  --processed data/processed \
  --index data/index.json \
  --metadata data/metadata.csv

# Optional: refresh one course after extractor-rule changes
python scripts/ingest.py --course BT2102

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

The graph UI reads `knowledge_base/graphs/graph.json` directly.

## Final submission

GitHub submission includes:

- source code in `src/`
- reproducible utility scripts in `scripts/`
- tests in `tests/`
- evaluation scripts and curated evidence in `evaluation/`
- refined concept pages in `knowledge_base/refined/`
- graph presentation bundles in `knowledge_base/graphs/`
- static website files in `website/`

Website viewing does not require raw PDFs or `data/`. Serve the repository root
over HTTP so browser `fetch()` calls work:

```bash
python3 -m http.server 8000
```

Open `http://127.0.0.1:8000/website/index.html`.

The PDF ingestion and full rebuild commands below are optional local workflows.
They require source PDFs and the installed PDF skill bridge; they are not needed
to view the submitted website.

## What stays local and unsubmitted

These paths remain local and are omitted from GitHub. Omission does not mean
permanent local deletion:

- `data/`
- `evaluation/runs/`
- `evaluation/workflow_test_report.md`
- `knowledge_base/concepts/`
- `knowledge_base/refined/`
- `knowledge_base/graphs/*.json`
- `knowledge_base/graphs/deltas/`
