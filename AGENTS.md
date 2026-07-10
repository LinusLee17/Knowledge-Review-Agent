# AGENTS.md

## Mission

The goal is to create a high-quality professional knowledge repository for:
* Business Analytics
* Machine Learning
* Statistics
* Data Science

This is done by building a durable knowledge base from lecture PDFs and supplementing it with your own resouces backed by reputable sources. Merge repeated material across courses into one coherent repository that remains usable after graduation.
Treat the repository as a persistent knowledge system, not a rebuild-on-every-run pipeline.

## Goals

- Extract structured notes from lecture PDFs.
- Merge duplicate concepts across sources.
- Normalize concept names to canonical keys before merging.
- Build concept relations for future navigation.
- Separate draft consolidation from presentation refinement.
- Render canonical concept pages in learning-flow order for study.
- Build graph state incrementally from canonical concept metadata.
- Keep provenance explicit at every step.
- Support human review when source evidence is weak.
- Process only new or modified PDFs during ingestion.
- Preserve lecture-level intermediate artifacts for downstream skills.

## Constraints

- Do not fabricate content.
- Do not drop source attribution.
- Do not mutate raw lecture PDFs.
- Do not normalize away important source detail.
- Do not implement quiz, flashcard, or interview features in MVP.
- Do not add graph visualization in MVP.
- Do not reprocess unchanged PDFs unless explicitly requested.
- Do not use CSV as long-term repository state.
- Do not let presentation refinement change technical meaning.
- Do not let evaluation run after refinement; evaluation must gate it.

## Coding standards

- Prefer small, explicit modules.
- Keep outputs deterministic and idempotent.
- Use ASCII by default.
- Use repo-local docs and schemas before inventing new conventions.
- Put shared logic in `src/knowledge_review_agent/` when it applies to more than one skill.
- Keep ingestion logic hash-driven and incremental.

## Expected outputs

- `data/raw/`: source PDFs only, kept untouched.
- `data/index.json`: repository-wide PDF state.
- `data/processed/<course>/<lecture>/lecture.md`: lecture-level Markdown.
- `data/processed/<course>/<lecture>/lecture.json`: lecture-level structured JSON.
- `knowledge_base/concepts/<concept>/concept.md`: canonical concept page in study-flow order.
- `knowledge_base/concepts/<concept>/metadata.json`: canonical provenance and versioning.
- `knowledge_base/graphs/`: graph node, edge, bundle, state, and delta data.
- `website/`: user-facing rendered knowledge site.
- `data/metadata.csv`: course mapping only, not primary repo state.

## Provenance rules

- Every derived note must record source file, course, lecture, and page.
- If multiple sources support a concept, list all of them.
- Canonical concept metadata must preserve contributing courses and lecture files.
- Keep original phrasing when exact wording matters.
- Preserve tables, equations, and figure references when they matter to meaning.
- Prefer additive consolidation over deletion of evidence.
- Put learning content before provenance and extraction metadata on concept pages.
- Presentation polish may reflow structure and formatting only.
- Preserve citations, provenance, and meaning through the presentation layer.

## Hallucination rules

- If source text is unclear, mark it unclear.
- If evidence is missing, leave a placeholder or review flag.
- Do not guess missing equations, labels, or table values.
- Do not merge concepts unless source overlap is strong enough to justify it.

## Source preservation rules

- Keep raw PDFs unchanged.
- Keep extracted text tied to source page numbers.
- Preserve section order when it carries meaning.
- Preserve original terminology alongside canonical concept names.
- Never overwrite source material with a cleaned summary.
- Leave unchanged concepts untouched during incremental updates.

## Human-in-the-loop

- Route uncertain extraction and concept merges to review.
- Prefer review notes over silent assumptions.
- Keep reviewer actions traceable.
- Quality gate failures must block presentation refinement until fixed.

## PDF skill rule

- Use the installed Anthropic PDF Skill. Do not use the OpenAI PDF Skill.
- Do not reimplement PDF parsing from scratch.
- Use local Python tooling only for repo orchestration, validation, and output shaping.

## Incremental ingestion rule

- Use `data/index.json` as ingestion state.
- Skip PDFs whose SHA-256 hash matches the stored value.
- Reprocess only new or modified PDFs unless `--rebuild-all` is explicit.
- Update only affected concept records and graph edges.
- Preserve previous concept versions and provenance.
- Treat concept consolidation as incremental: rewrite only affected concept files.
- Treat graph building as incremental: rewrite only affected nodes and edges.
- Write `knowledge_base/graphs/graph.json` as the presentation bundle consumed by the website.
- Keep draft and refined knowledge bases separate.

## External Skill Dependencies

This project relies on the following installed Codex Skills:

- Anthropic PDF Skill
  - Used exclusively for PDF parsing and document inspection.

- Impeccable Skill
  - Used exclusively for presentation refinement after evaluation has completed.

These Skills are treated as external agent capabilities and should not be replaced with custom implementations.
