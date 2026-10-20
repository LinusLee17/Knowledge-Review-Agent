# Evaluation and publication eligibility

Evaluation precedes presentation preparation. `evaluate_consolidation()` still
returns heuristic diagnostics; it is not an LLM judge or factual-accuracy proof.
The command now also creates source-bound eligibility evidence through the shared
quality gate. A score of 100 cannot override missing definitions or provenance.

```bash
python evaluation/evaluate_consolidation.py \
  --concepts knowledge_base/concepts \
  --processed data/processed \
  --reviews evaluation/reviews \
  --asset-root data/raw \
  --reports evaluation/runs/gates
```

Exit 0 means eligible; exit 1 means blocked/failed; argparse usage errors use 2.
JSON output includes report path, eligibility, findings, and diagnostic metrics.
Reports are immutable content-addressed JSON. Failed reports remain evidence.
No local corpus is automatically repaired, refined, or approved.

Hard blockers include empty/incomplete/invalid or duplicate records, missing or
mismatched definitions/classification, missing provenance, unsafe/unreadable
sources/assets, wrong lecture hashes/course/page support, and pending persistence
recovery. Source support requires an explicit structured concept/candidate on a
positive source page, not a filename or an arbitrary text substring.

Linked local assets must lie within declared concept/history/processed/asset
roots. Inline links and reference-style definitions share dependency capture and
rebasing, including angle paths, balanced path parentheses and quoted titles.
Repeat `--asset-root` for other evidence locations. Raw PDFs may be hashed
as linked assets; no PDF parser or raw-file mutation occurs here. External links
are retained without fetching or certification.

## Human review records

Persistence conflicts, nonempty Quality Review sections, and weak-definition
heuristics require explicit human disposition. Records are human-written JSON
under `evaluation/reviews/`, named `<record_id>.json`. Do not invent a reviewer,
rationale, timestamp, or approval to make evaluation pass.

Required top-level fields:

- `schema_version`: integer 1.
- `reviewer`, `reviewed_at`, `rationale`: nonempty identity, ISO UTC timestamp,
  and explanation of the real review.
- `concept_key`, `concept_fingerprint`: exact concept identity from current report.
- `resolutions`: nonempty list with `finding_id`, `finding_digest`, `disposition`,
  and `citations` for each reviewed finding.
- `record_id`: SHA-256 of canonical payload excluding `record_id` itself.

Each disposition is `accepted_with_evidence` or `not_applicable`; each citation
has a processed-root-relative `lecture_file` and positive integer `page_number`
from that concept's supported source pages. `finding_digest` is the canonical
SHA-256 of that finding's `details`. Identifiers and JSON canonicalization use
`quality_gate.content_digest`: sorted keys, ASCII escaping, compact separators,
UTF-8 bytes, no nonfinite numbers.

Hard failures cannot be reviewed away. Partial coverage, malformed records,
unsupported citations, or contradictory current dispositions block. Valid older
records stay as history but cannot resolve current findings. Concept review
fingerprints exclude review bytes to avoid self-reference; the corpus report
includes review-file inventory so changed/new decisions invalidate old reports.
No authenticated identity or signature system is claimed.

After completing a real review or fixing a draft, reevaluate before refining:

```bash
python scripts/refine_concepts.py \
  --concepts knowledge_base/concepts \
  --refined knowledge_base/refined \
  --evaluation evaluation/runs/gates/<report-id>.json
```

Use the actual passing report path printed by evaluation. Missing, failed,
malformed, wrong-policy, or stale reports fail before publication writes.
Changes to draft membership/content, source artifacts, assets, review records,
or persistence state require reevaluation. No arbitrary report expiry applies.
No force/skip-gate option exists. Old metrics-only reports are not approvals.

Reports include schema/policy versions, evaluator kind, root identities, complete
input manifest/digest, concept fingerprints/support pages, findings/resolutions,
review references, metrics, eligibility, and content-derived report ID. Reports
must be outside input and refined roots. Keep reports and review history locally;
GitHub exclusion never authorizes deletion.

## Preservation and limits

Refinement prepares all requested outputs from evaluated bytes, preserves raw
metadata JSON (including unknown keys), equations, tables, citations, and section
occurrences, then rechecks input roots, dependency bytes, record/review/journal
membership and path safety before publishing changed files. This final check
does not rerun content evaluation after formatting.
Unchanged output is not rewritten. Content/freshness failures publish nothing.
Deterministic formatting is a preparation utility; no new Impeccable adapter or
LLM evaluator is implemented. The required external skills remain separate.

Local single-writer execution is required. Final file writes are individually
atomic; a filesystem error during multi-file publication may leave partial
updates and is reported. Website viewing needs neither evaluation nor raw data.
Graph integrity diagnostics remain available through `evaluate_graph.py`; those
structural checks do not validate relation truth or missing-relationship recall.

## Shared source policy (gate policy 2)

Gate uses shared source occurrences from already captured lecture bytes. Accepted
structured labels include `concept_name`, `concept_label`, `name`, `title` and
explicit aliases; an explicit canonical key cannot be overridden by an unrelated
display-name match. Candidate labels establish page presence; raw text search
alone cannot. Course identity uses course ID, otherwise course name.

Duplicate/out-of-range/invalid page numbers, non-finite/duplicate-key JSON and
conflicting item source page/PDF declarations are hard source failures. These
failures produce retained blocked reports. Supported-page and reviewer citation
JSON shapes remain unchanged (schema 1); current readiness uses policy `3`.
Policy 3 rejects leading TODO/TBD definitions and tracks evidence links with
nested or escaped labels. Reports from earlier policies require reevaluation.
Old policy-1 reports must be reevaluated, and old review fingerprints do not count
as current approvals. No automatic conversion or approval is generated.

## Graph presentation checks

`python3 evaluation/evaluate_graph.py --presentation` validates graph.json plus
actual refined metadata/Markdown/viewer targets. It requires no drafts, data/,
internal nodes/edges or readiness report. Success prints valid/schema_version/
node_count/edge_count; malformed/missing graph or invalid target returns 1 with
structured error/issues. Without --presentation, existing internal heuristic
metrics remain unchanged and are not a presentation contract certificate.
