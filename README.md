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
   - Heuristic diagnostics plus explicit source/course/page/hash checks
   - Content-bound evaluation reports and traceable human review decisions
   - Blocks refinement on missing, failed, or stale eligibility evidence

4. `presentation_refinement`
   - Gated deterministic preparation: reorders sections without changing content
   - Impeccable remains an external capability; no executable adapter is claimed

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
```

Website viewing, tests, and evaluation do not need the PDF skill command.
Set it only for optional PDF ingestion or full rebuilds, using the local PDF
skill runtime path:

```bash
export ANTHROPIC_PDF_SKILL_COMMAND="$(command -v python3) $(pwd)/scripts/pdf_skill_bridge.py"
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
  --concepts knowledge_base/concepts \
  --processed data/processed \
  --reviews evaluation/reviews \
  --asset-root data/raw \
  --reports evaluation/runs/gates

# Use the passing report path printed by evaluation. Blocked findings must be
# fixed or explicitly reviewed where allowed, then evaluated again.
python scripts/refine_concepts.py \
  --concepts knowledge_base/concepts \
  --refined knowledge_base/refined \
  --evaluation evaluation/runs/gates/<report-id>.json

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

Evaluation reports bind exact draft, source, asset, review, and policy identities.
Changing any evaluated input requires a new report. Scores do not override hard
failures; a passing report checks readiness and source references, not full
factual correctness. See `evaluation/README.md` for human review records.
The evaluator does not parse PDFs; `--asset-root` only permits hashing linked
local evidence. Old refinement commands without `--evaluation` now fail closed.

## Final submission

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

## What stays local

These paths remain local and are omitted from GitHub:

- `data/`
- `evaluation/runs/`
- `evaluation/reviews/`
- `evaluation/workflow_test_report.md`
- `knowledge_base/concepts/`
- `knowledge_base/graphs/deltas/`

Source occurrence tracking is shared across consolidation, quality audit and
evaluation. Identical evidence text retains all original source locations. Draft
repair requires declared lecture hashes and explicit page support; audit reports
full coverage separately from capped display groups. Gate policy 2 requires fresh
evaluation of older policy-1 reports. See [evaluation guidance](evaluation/README.md)
and [script guidance](scripts/README.md). No new persistent index or PDF rebuild.

Graph presentation now exports schema 2 from matching refined records. Website
loads only validated graph.json; complete legacy schema-1 bundles remain supported.
Use `python3 evaluation/evaluate_graph.py --presentation` for published structural
and file checks. This differs from internal heuristic metrics and does not certify
knowledge correctness or rerun readiness evaluation.
