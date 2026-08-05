# Final Submission Cleanup Design

## Goal

Prepare a clean GitHub submission that contains a functional concept website with graph visualization, source code, tests, evaluation evidence, and concise reproduction instructions, while preserving excluded local artifacts.

## Submission boundary

The GitHub submission will include:

- `src/` source code.
- `scripts/` required reproducible utilities, excluding one-off tooling when proven unused.
- `tests/` and test documentation.
- `evaluation/` evaluation scripts plus a concise, curated evidence report.
- `website/` frontend source.
- `knowledge_base/refined/` refined concept pages and metadata required by the website.
- `knowledge_base/graphs/graph.json`, `nodes.json`, and `edges.json` required by the graph UI.
- README, architecture/schema documentation, requirements, and relevant project instructions.

The submission will not require `data/`, raw lecture PDFs, or PDF parsing to view the website. Reproduction instructions will describe the website-only path separately from the optional full ingestion path.

## Local preservation

Files excluded from GitHub will be classified and omitted from Git tracking or submission packaging. They will not be permanently deleted. Candidate local-only material includes raw PDFs, processed lecture artifacts, draft concepts, old evaluation runs, caches, `__pycache__`, `.DS_Store`, and temporary design/output files.

## Cleanup method

1. Build a file inventory and classify each path as submission-required, local-only, generated-but-required, archive-only, or unused.
2. Trace imports, CLI references, README references, website fetch paths, tests, and evaluation dependencies before changing tracking.
3. Preserve required website inputs even when generated.
4. Remove only approved clutter from GitHub scope; preserve local copies.
5. Update README and ignore rules so a clean checkout has clear setup and website instructions.
6. Run lightweight structural and website checks first.
7. Ask for approval before PDF parsing, dependency installation, full test suites, or other heavy validation.
8. Run final verification after approved checks.

## Website behavior

The website must render refined concept pages and graph visualization from checked-in generated presentation inputs. It must not read or rebuild from `data/` in the browser.

## Quality constraints

- Preserve provenance and source attribution in refined concept metadata.
- Keep evaluation before presentation refinement in the documented workflow.
- Do not alter technical meaning during cleanup.
- Do not silently delete evidence or local source material.
- Keep changes deterministic and reviewable on branch `superpowers-dev`.
