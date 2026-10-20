# Final Submission Cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a clean GitHub submission with source code, tests, curated evaluation evidence, concise reproduction instructions, and a functional website with graph visualization, while preserving excluded files locally.

**Architecture:** Keep executable source and tests tracked. Check in only generated presentation inputs required by the website: refined concepts and graph bundles. Keep raw PDFs, processed lecture artifacts, drafts, caches, and historical runs local and ignored. Make website-only viewing independent of `data/`.

**Tech Stack:** Python, pytest, static HTML/CSS/JavaScript, Markdown/JSON, Git.

---

### Task 1: Capture the submission file manifest

**Files:**
- Create: `docs/submission_manifest.md`

- [ ] **Step 1: Record required tracked paths**

  Document `src/`, required `scripts/`, `tests/`, `evaluation/` scripts and curated evidence, `website/`, refined concept pages, graph bundle JSON, README, docs, requirements, and project instructions.

- [ ] **Step 2: Record local-only paths**

  Document `data/`, raw PDFs, processed lecture artifacts, canonical draft concepts, old `evaluation/runs/`, caches, `__pycache__`, `.DS_Store`, and one-off design artifacts as preserved local files excluded from GitHub.

- [ ] **Step 3: Verify manifest paths exist without parsing PDFs**

  Run:

  ```bash
  test -d src && test -d tests && test -d website && test -d knowledge_base/refined
  test -f knowledge_base/graphs/graph.json
  ```

  Expected: exit code `0`. If a required generated path is absent, stop and report it; do not regenerate through PDF parsing.

### Task 2: Make website presentation outputs trackable

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Add narrow Git exceptions**

  Preserve broad ignores for local data and generated outputs, then allow only `knowledge_base/refined/**` and `knowledge_base/graphs/graph.json`, `nodes.json`, and `edges.json` to be included in the submission.

- [ ] **Step 2: Verify ignore behavior**

  Run:

  ```bash
  git check-ignore -v data knowledge_base/concepts knowledge_base/refined/"Gradient Descent"/concept.md knowledge_base/graphs/graph.json
  ```

  Expected: `data` and canonical concepts remain ignored; refined concept and required graph bundle paths are not reported as ignored.

### Task 3: Update concise reproduction instructions

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add submission contents section**

  State that the repository includes source, tests, evaluation evidence, refined presentation outputs, and graph visualization inputs. State that raw PDFs and `data/` are not needed for website viewing.

- [ ] **Step 2: Add website-only run instructions**

  Document:

  ```bash
  python3 -m http.server 8000
  ```

  Then open `http://127.0.0.1:8000/website/index.html` and explain that static serving is required for `fetch()` requests.

- [ ] **Step 3: Separate optional pipeline instructions**

  Mark ingestion/PDF commands as optional local rebuild workflow requiring external PDF skill setup. Do not claim clean-checkout ingestion works without source PDFs.

### Task 4: Preserve evaluation evidence without historical run clutter

**Files:**
- Create or modify: `evaluation/submission_evidence.md`
- Keep: `evaluation/evaluate_consolidation.py`
- Keep: `evaluation/evaluate_graph.py`

- [ ] **Step 1: Select existing evidence only**

  Use existing local evaluation reports and summaries. Record source path, date/run identifier, checks performed, and observed result. Do not invent scores or rerun evaluation.

- [ ] **Step 2: Make evidence concise**

  Include quality-gate order, provenance checks, graph checks, and links to the relevant scripts. Keep full historical runs local under `evaluation/runs/`.

### Task 5: Remove tracked-only clutter from GitHub scope

**Files:**
- Candidate tracked paths: `.impeccable/`, `Knowledge-Review-Agent-overview-edited.excalidraw`, `scripts/create_overview_excalidraw.py`

- [ ] **Step 1: Verify each candidate has no submission dependency**

  Search README, docs, scripts, tests, and website references before changing tracking.

- [ ] **Step 2: Untrack approved candidates while preserving local files**

  Use `git rm --cached -- <path>` only for candidates confirmed unused and not needed by final documentation. Do not use filesystem deletion commands.

- [ ] **Step 3: Confirm local preservation**

  Verify excluded candidate files remain on disk after index changes.

### Task 6: Stage required generated presentation artifacts

**Files:**
- Add to GitHub scope: `knowledge_base/refined/**`
- Add to GitHub scope: `knowledge_base/graphs/graph.json`, `nodes.json`, `edges.json`

- [ ] **Step 1: Inspect artifact counts and size**

  Run metadata-only file counts and sizes. Do not open every concept page or parse PDFs.

- [ ] **Step 2: Stage only approved presentation outputs**

  Use explicit paths and `git add -f` only where ignore rules still require it.

- [ ] **Step 3: Review staged path list**

  Confirm no raw PDFs, `data/`, draft concepts, old runs, caches, or temporary files are staged.

### Task 7: Run lightweight verification

**Files:**
- No source changes expected.

- [ ] **Step 1: Verify website references resolve structurally**

  Check required HTML/JS/CSS files and graph bundle paths. Do not run a browser automation or rebuild.

- [ ] **Step 2: Verify Git submission boundary**

  Inspect `git diff --cached --name-status` and `git status --short --ignored`.

- [ ] **Step 3: Request approval before heavy checks**

  Before running dependency installation, the full pytest suite, website browser testing, evaluation scripts, or any PDF-related task, report expected cost and ask the user for approval.

- [ ] **Step 4: Commit only after review**

  Commit cleanup changes with a focused message after the user approves the staged diff.
