# Presentation preparation

`scripts/refine_concepts.py` and both public Python refinement entry points require
a current passing eligibility report. Example:

```bash
python scripts/refine_concepts.py --evaluation evaluation/runs/gates/<report-id>.json
```

The shared gate binds exact drafts, source evidence, assets, review decisions, and
policy versions. Missing/failed/stale evidence blocks before writing output.
A high heuristic score never bypasses hard failures or unresolved review findings.
See `evaluation/README.md` for evaluation commands and human review schema.

Preparation reorders sections without changing technical content, keeps repeated
sections and code fences, preserves raw metadata JSON, and rebases local asset
links to the same targets. All requested outputs are staged and freshness is
checked before changed files publish. Drafts stay separate from refined output.
Audit/repair writes drafts only; it cannot patch publication directly.

This executable remains a deterministic preparation utility. Impeccable is the
external presentation capability required by project instructions; no callable
adapter is claimed or replaced by this change. Any future external adapter must
cross the same eligibility seam and preserve meaning, equations, citations, and
provenance. Do not run content evaluation after preparation.

Scope: local single writer. Publication files replace atomically one at a time;
a filesystem failure can leave partial output and must be reported. Generated
content is not a complete factual-accuracy certificate.
