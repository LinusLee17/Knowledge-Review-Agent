# Evaluation-to-refinement seam

Status: implemented on 2026-10-19 after user approval; verified with 117 tests and one fresh-context review plus regression fixes.

## Intended outcome

The selected architecture-review candidate is evaluation-to-refinement eligibility.
A refined page may be written only when evaluation passed for the exact current
draft corpus, relevant source artifacts, review decisions, and gate policy.
Missing, failed, malformed, or stale evaluation blocks supported refinement
commands and functions before they modify published output.

This is architectural work: it changes the interface between evaluation and
refinement and closes another command's direct publication path. Preserve the
completed persistence implementation and current `superpowers-dev` checkout.

## Pre-change behavior and risks

- `evaluate_consolidation` returns diagnostic heuristics, not a persisted
  eligibility decision. Its aggregate score can reach 100 with missing content.
- `evaluation/evaluate_consolidation.py` always exits successfully after printing
  metrics and produces no evidence artifact consumed by refinement.
- Both `refine_concepts` and `refine_concept_page` can write without evaluation.
- `scripts/audit_repair_concepts.py --apply` edits refined content directly, after
  changing drafts, bypassing both the proposed gate and draft/refined separation.
- Persistence conflicts and `Quality Review` sections exist, but publication
  does not inspect them.
- Existing refinement is a deterministic section-ordering utility. It does not
  invoke Impeccable. Do not present this utility as an external-skill adapter.

## Approaches

1. **Recommended: persisted eligibility report plus shared enforcement module.**
   Evaluation captures input identities, hard failures, and review status.
   Refinement validates that report against current inputs before generating
   output. All supported publication entry points share one policy.
2. **Reevaluate automatically inside refinement.** Fewer explicit commands, but
   hides evaluation work, complicates review evidence, and risks evaluating
   different bytes from those rendered. Defer rather than duplicate policy.
3. **CLI sequencing only.** Small change, but direct Python callers and the repair
   command still bypass it. Does not meet the repository's quality-gate rule.

## Module responsibilities

- New `quality_gate.py`: shared draft discovery, input manifests, policy checks,
  traceable review resolution, report validation, and eligibility failures.
- `evaluation.py`: existing heuristic and recall metrics remain diagnostics;
  their public result shapes remain compatible. They do not grant publication.
- `evaluation/evaluate_consolidation.py`: run pre-refinement evaluation, persist
  its evidence report, print actionable findings, and return nonzero when blocked.
- `presentation_refinement.py`: require valid eligibility, prepare presentation
  from the evaluated bytes, and preserve meaning and metadata. Make ungated
  formatting helpers private; supported public functions enforce eligibility.
- `scripts/refine_concepts.py`: require the evaluation report path and delegate
  enforcement to the same module as Python callers.
- `scripts/audit_repair_concepts.py`: repair drafts only, through the existing
  persistent record store. Publish nothing; repaired bytes require evaluation
  again. Preserve existing refined files until separately approved refinement.

No database, new runtime dependency, browser UI, or generic workflow framework.

## Input identity and discovery

Use one deterministic discovery policy for evaluation and refinement. Every
candidate must have both `concept.md` and `metadata.json`; incomplete records,
unreadable files, ambiguous nested records, duplicate canonical keys, and unsafe
symlinked paths are explicit blockers rather than silent skips. An empty or
missing concepts root cannot pass.

The inventory captures sorted root-relative paths and SHA-256 values for:

- all draft Markdown and metadata records and their membership;
- local evidence assets referenced by draft pages, including retained archive
  assets, within explicitly configured draft/history/source roots;
- every contributing processed `lecture.json` used as provenance;
- the explicit reviewer decision records used to resolve findings;
- gate policy version and report schema version.

Record resolved input-root identities in the report. New/deleted/renamed concepts,
Markdown-only edits, metadata changes, changed evidence assets, changed lecture
bytes, and changed review decisions invalidate prior eligibility. Unrelated
evaluation reports and archive records are not active concepts.

Resolve local references against their original page locations. Reject path
escapes and unsupported symlink references. External reading links are preserved
but are not fetched or certified. Do not parse or modify raw PDFs.

Pending persistence transactions block evaluation. The gate is read-only and
must not recover or repair drafts; report the need to run consolidation recovery
before evaluating again.

## Readiness policy

Hard failures are never overridden by a high score or review acknowledgment:

1. Missing/incomplete/invalid corpus or concept records; duplicate canonical keys.
2. Missing concept identity, domain/topic classification, or usable definition in
   either metadata or the Markdown `Definition` section. Literal name-only and
   explicit placeholder definitions are not usable. Meaningful definition text
   must agree across Markdown and metadata after whitespace normalization.
3. Missing contributing courses, lecture references, or lecture hashes.
4. Missing, unreadable, unsafe, or hash-mismatched contributing lecture artifacts.
5. No positive source-page reference supporting the canonical concept within a
   contributing lecture's structured concepts or explicit concept candidates.
   Source course attribution must agree with contributing-course metadata.
6. Unsafe/missing local evidence assets or unverifiable pending persistence state.

Inspect every listed contributing lecture. Report supported pages and attribution
per concept; do not infer support from a lecture filename or arbitrary prose
substring alone. Source-page support is a reference check, not a claim that every
sentence or equation has been factually verified.

The following require human disposition before passage:

- current persistence conflicts;
- nonempty `Quality Review` content;
- definitions flagged weak by the existing definition-quality heuristic.

Empty optional sections such as mathematical foundations do not automatically
mean incorrect content. Existing quality-review flags remain visible and require
an explicit disposition when a reviewer concludes an item is not applicable.
No mandatory aggregate-score threshold is introduced. Existing metrics remain
diagnostic and are honestly labeled heuristic, not LLM-as-a-Judge.

## Traceable review decisions

Use local JSON review records under `evaluation/reviews/`; no review interface
or automatically generated approvals. Each record must identify:

- schema version, reviewer identity, reviewed-at UTC timestamp, and rationale;
- concept key and exact reviewed draft/source fingerprint;
- exact finding identifiers and finding-content digests being resolved;
- disposition (`accepted_with_evidence` or `not_applicable`) and cited source
  lecture/page evidence for each finding.

Review records can resolve discretionary review findings only. They cannot
override hard failures, remove source attribution, or hide historical conflict
alternatives. Missing coverage, malformed records, contradictory dispositions,
or records bound to older bytes remain blocked. Keep review records append-only
using content-derived record identities, and include referenced decisions in
evaluation evidence. Record history separately from the current decision.

This is a local trusted review record, not authenticated identity or a signature.
No approval is fabricated during tests, evaluation, or refinement; synthetic
review records are allowed only in test temporary directories.

## Evaluation report

The report records schema/policy versions, evaluator kind, resolved input roots,
full input manifest and digest, diagnostic metrics, per-concept findings,
review references, and explicit eligibility (`pass` or `blocked`). Findings have
stable codes, affected concept/path, evidence details, and remediation guidance.

Use deterministic JSON and content-derived report identity. Save reports outside
draft/refined inputs, normally under `evaluation/runs/gates/`. Retain failed
reports as evidence. Reuse an identical existing report only after verifying its
contents; never silently replace differing evidence at the same identity.

Validate report schema and content identity, supported policy version, decision
consistency, input roots, and current manifest before accepting it. A legacy
metrics-only report, edited decision, copied `pass` field, or missing findings
cannot stand in for an eligible report. This protects against stale/corrupt
artifacts, not a malicious operator who can rewrite all local inputs and hashes.

No arbitrary time-to-live: unchanged inputs and policy retain eligibility.
Reviewer timestamps provide traceability, not a substitute for content freshness.

## Refinement enforcement

1. Reject missing/invalid/blocked/stale reports before creating or modifying any
   refined concept directory.
2. Reject equal or overlapping draft/refined roots, reports stored inside either
   root, and unsafe output paths before writing.
3. Load evaluated input bytes into a stable in-memory preparation snapshot.
   Prepare every affected output in temporary staging without changing drafts
   or existing refined output.
4. Validate that formatting preserves section content, equations, tables,
   citations, provenance, and raw metadata values. Heading aliases and order may
   change; no technical claims may be inserted, removed, or rewritten. The
   metadata output copies the approved input bytes rather than dropping unknown
   fields through model serialization.
5. Recheck the input manifest immediately before publication. Any change since
   evaluation or preparation blocks the run without touching refined output.
6. Write only changed prepared outputs; unchanged output bytes retain their file
   modification times. Report failures explicitly and retain drafts and existing
   output on eligibility/preparation failures.

The gate always precedes refinement. Freshness checks and transformation
invariants during preparation are not a post-refinement content evaluation.
Do not run the content evaluator after presentation generation.

Scope remains local single-writer operation. Validation failure produces no
publication writes. A filesystem failure during final multi-file publication may
leave partial updated output and must be reported; this change does not promise
a new corpus-wide publication transaction or concurrent-writer protection.

The existing deterministic formatter remains a preparation utility. Impeccable
continues to be the external presentation capability required by project rules;
this change does not implement, replace, or claim a new Impeccable adapter. Any
future external presentation adapter must cross the same eligibility seam.

## CLI and compatibility

- Evaluation accepts concept/source roots and review-record location, writes a
  report, and returns exit 0 only for a passing evaluation. Blocked/input errors
  return nonzero with actionable JSON findings.
- Refinement requires `--evaluation <report-path>`. Existing commands without a
  report fail before output changes; there is no force/skip-gate option.
- Both existing public Python refinement entry points enforce the same rule;
  old calls without evaluation evidence fail clearly and without side effects.
- Audit/repair `--apply` becomes draft-only. Existing `--refined` handling must
  not retain a hidden write path; document its removal or clear rejection.
- Preserve existing diagnostic metrics functions and website-only setup. Viewing
  the submitted site does not require evaluation, raw PDFs, or local `data/`.

## Verification

Use temporary synthetic draft/lecture/review artifacts. Never evaluate, repair,
or refine the production corpus to make the tests pass.

- Missing/blocked/stale/tampered reports fail through CLI and Python entry points
  without modifying preexisting refined bytes or creating concept directories.
- Markdown-only edits, metadata edits, concept additions/removals/renames,
  changed lecture bytes, asset edits, and changed review decisions invalidate a
  previously passing report, even if version numbers remain unchanged.
- Empty definitions and nonexistent lecture references cannot pass despite an
  aggregate heuristic score of 100. Cover duplicate, incomplete, empty, and
  unsafe/symlinked input cases explicitly.
- Review findings block until exact current evidence-backed dispositions exist;
  stale, partial, conflicting, or attempted hard-failure overrides remain blocked.
- Repair apply leaves refined content untouched, preserves previous draft bytes
  through the record store, and invalidates old evaluation.
- A valid report permits formatting with unchanged technical content, unknown
  metadata fields, source links, equations, and tables. Unchanged reruns do not
  rewrite outputs. Cover headings inside code blocks and repeated/aliased
  sections so formatting cannot silently discard or duplicate content.
- Mutation during preparation blocks before final writes. Report/output overlap
  and malformed/tampered artifact identities fail without side effects.
- Keep all existing persistence tests green. Update old refinement fixtures to
  include actual synthetic source provenance and evaluation evidence.

## Delivery boundary

Update architecture, evaluator/refinement guidance, README commands, test guidance,
and submission exclusions to reflect actual behavior. `evaluation/reviews/` and
generated reports are local evidence; exclusion never authorizes deletion.

No quality-score recalibration, LLM judge integration, source extraction changes,
graph fixes, or website redesign. Native execution preference carries forward;
after written-spec approval, prepare implementation plan for review before
runtime edits. Preserve prior persistence work and unrelated untracked image.
