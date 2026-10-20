# Evaluation-to-Refinement Seam Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Native execution and plan approved by user on 2026-10-19.

**Goal:** Allow refinement writes only when a verifiable passing evaluation matches current drafts, source evidence, reviewer decisions, and gate policy.

**Architecture:** A shared gate module owns input snapshots, readiness findings, review resolution, and immutable evaluation reports. Evaluation creates evidence; refinement consumes it and formats the evaluated bytes. A shared lossless Markdown reader prevents evaluator/formatter disagreement, and repair operates only on persistent draft records.

**Tech Stack:** Existing Python, dataclasses, standard-library JSON/SHA-256/path tooling, pytest. No new runtime dependencies or network calls.

**Spec:** [Approved evaluation-to-refinement spec](../specs/2026-10-19-evaluation-refinement-seam-design.md)

## Global Constraints

- Preserve the completed persistence implementation and current `superpowers-dev` checkout.
- No database, new runtime dependency, browser UI, or generic workflow framework.
- Do not parse or modify raw PDFs.
- Review records can resolve discretionary review findings only.
- No mandatory aggregate-score threshold is introduced.
- The gate always precedes refinement.
- No arbitrary time-to-live: unchanged inputs and policy retain eligibility.
- No approval is fabricated during tests, evaluation, or refinement; synthetic review records are allowed only in test temporary directories.
- Scope remains local single-writer operation.
- Validation failure produces no publication writes.
- No quality-score recalibration, LLM judge integration, source extraction changes, graph fixes, or website redesign.
- Preserve prior persistence work and unrelated untracked image.
- Git staging was sandbox-blocked during persistence work. Keep task changes reviewable and uncommitted under that existing fallback; no push or merge.

## Review Focus

1. Review history must remain append-only: stale decisions cannot resolve current findings, but older valid records must not prevent a newer valid decision from passing (Task 3).
2. Markdown headings inside fenced code, duplicate/aliased sections, and local links with fragments/titles must retain content and resolve to the same evidence after formatting (Tasks 1 and 4).
3. Missing source pages, mismatched course attribution, or candidate labels unrelated to the concept must block even when every referenced file exists (Task 2).
4. Every supported write route, including single-page Python calls and audit/repair apply, must enforce the same separation; a failure on the last concept cannot partially publish earlier prepared pages (Tasks 4 and 5).
5. Reports and reviews must not depend circularly on their own hashes; mutated assets, new/removed concepts, changed review membership, and pending persistence journals must invalidate passage without modifying inputs (Tasks 2 and 3).

## File Map and Shared Decisions

| File | Responsibility |
| --- | --- |
| `src/knowledge_review_agent/concept_document.py` (new) | Lossless, fence-aware section parsing; local link discovery; deterministic reordering; transformation invariants. |
| `src/knowledge_review_agent/quality_gate.py` (new) | Input collection, readiness findings, review/report schemas, eligibility validation. Keep one shared policy, not separate CLI/Python versions. |
| `src/knowledge_review_agent/evaluation.py` | Existing metrics remain compatible diagnostics; expose definition-quality helper if required, without importing its private implementation elsewhere. |
| `src/knowledge_review_agent/presentation_refinement.py` | Gate supported entry points, stage approved output, validate freshness, write changed bytes only. |
| `evaluation/evaluate_consolidation.py`, `scripts/refine_concepts.py` | CLI adapters to the same gate interfaces. |
| `scripts/audit_repair_concepts.py` | Draft-only audit/repair via existing record store; no direct refined writes. |
| `tests/gate_fixtures.py` (new) | Synthetic valid draft/source/report/review fixtures shared by gate and refinement tests. |
| `tests/test_concept_document.py`, `tests/test_quality_gate.py`, `tests/test_gate_commands.py` (new) | Parser, policy, artifact, and command regressions. |
| `tests/test_presentation_refinement.py` | Publication enforcement, preservation, and no-op coverage. |
| README, architecture/evaluation/refinement/test guidance, submission manifest, `.gitignore` | Reproduction, truthful capability descriptions, local evidence exclusions. |

**Input types:** Define frozen `GatePaths(concepts_root: Path, processed_root: Path, reviews_root: Path, asset_roots: tuple[Path, ...] = ())`, `GateConcept(relative_dir: str, concept_key: str, markdown: bytes, metadata: bytes, fingerprint: str)`, and `GateSnapshot(paths: GatePaths, manifest: dict[str, str], fingerprint: str, concepts: tuple[GateConcept, ...], findings: tuple[GateFinding, ...])` in `quality_gate.py`.

**Finding type:** Define frozen `GateFinding(code: str, concept_key: str, path: str, severity: str, details: dict, remediation: str, finding_id: str, resolved_by: tuple[str, ...] = ())`. Severity is exactly `hard` or `review`. Finding identity hashes code, concept, affected path, and exact details, excluding resolution and report identity.

Use `GateError(RuntimeError)` for rejected eligibility, artifact, or input configuration. CLI adapters return exit 1 for blocked/failed runs and argparse's exit 2 for usage errors; exit 0 means success. Preserve existing diagnostic result types.

**Identity separation:** A concept fingerprint covers its draft bytes and source/asset dependencies plus policy version, excluding review records. Corpus fingerprint covers sorted membership and all input dependencies, including review inventory. Review and report IDs hash their canonical JSON payload excluding only their own ID field. No timestamp-only freshness checks.

---

### Task 1: Shared Lossless Document Parsing and Evidence Links

**Files:** Create `concept_document.py`, `tests/test_concept_document.py`; no publication behavior change yet.

**Interfaces:**
- Produce frozen `DocumentSection(heading: str, content: str)` and `ConceptDocument(prefix: str, title: str, sections: tuple[DocumentSection, ...])`.
- Produce `parse_concept_document(markdown: str) -> ConceptDocument`.
- Produce `local_document_links(markdown: str) -> tuple[str, ...]`, preserving destination/query/fragment identity and ignoring external URLs and page-only anchors.
- Produce `format_concept_document(markdown: str) -> str` and `assert_presentation_preserved(original: str, formatted: str) -> None`.

- [x] **Step 1: Write parser/invariant tests.**

  `test_fences_and_duplicate_sections_preserve_content`: include YAML prefix,
  an H1 title, two Definition sections, Applications/Real-world Applications
  aliases, equations, tables, and fenced snippets containing `#`/`##` lines.
  Assert code lines remain content; duplicate section bodies each survive once;
  front matter remains exact; alias ordering does not concatenate distinct
  bodies silently; formatting twice produces identical bytes.

  `test_local_links_preserve_targets_fragments_and_titles`: include relative
  image/file links with percent encoding, angle-bracket destinations, titles,
  fragments, HTTP links, and anchors. Assert only local file destinations are
  returned, without treating fenced examples as actual asset dependencies.

  `test_transform_invariant_rejects_changed_claims`: changing/deleting equation,
  citation, table cell, or repeated section fails. Reordering sections and
  changing supported heading aliases passes. Nonblank body content must remain
  exact after newline normalization; do not collapse table/equation whitespace.

- [x] **Step 2: Run `pytest tests/test_concept_document.py -q`; observe intended missing-interface failures.**
- [x] **Step 3: Implement interfaces.** Reuse existing canonical order/aliases by moving their shared definitions here and retaining compatibility imports from refinement. Keep ordered section occurrences rather than a heading-keyed dictionary. Parse fences before interpreting headings/links. Preserve unfamiliar content rather than discarding it; reject ambiguous/unclosed structures if preservation cannot be proven.
- [x] **Step 4: Run `pytest tests/test_concept_document.py tests/test_presentation_refinement.py -q`; require green tests.**
- [x] **Step 5: Inspect diff and run `git diff --check`.** Conditional commit if available: `refactor: share lossless concept document handling`.

### Task 2: Capture Exact Inputs and Derive Readiness Findings

**Files:** Create `quality_gate.py`, `tests/gate_fixtures.py`, `tests/test_quality_gate.py`; modify `evaluation.py` only to expose an existing helper without changing score behavior.

**Interfaces:**
- Consume Task 1 parsing and local-link discovery plus existing metadata reader and `concept_history_root`.
- Produce shared types above and constants `GATE_SCHEMA_VERSION = 1`, `GATE_POLICY_VERSION = "1"`.
- Produce `capture_gate_snapshot(paths: GatePaths) -> GateSnapshot` and `evaluate_readiness(snapshot: GateSnapshot) -> tuple[GateFinding, ...]`.
- Produce `evaluate_definition_quality(metadata: ConceptMetadata) -> float` in `evaluation.py`; preserve `_definition_quality` compatibility internally if needed.

- [x] **Step 1: Add synthetic fixtures and failing policy tests.**

  `test_valid_source_backed_corpus_has_no_hard_findings`: build complete metadata,
  matching Markdown definition, real synthetic lecture JSON with matching course,
  canonical concept, positive page number, and actual lecture SHA-256. Capture
  without creating/changing any input file. Assert deterministic snapshots.

  `test_hard_failures_cannot_hide_behind_perfect_score`: parameterize empty/name-only/
  placeholder definitions, metadata/Markdown disagreement, missing classification,
  missing/invalid hashes, nonexistent lecture, unsupported page, wrong course,
  duplicate key, partial/nested record, empty/missing corpus, and symlink escapes.
  Assert stable actionable hard findings, including a fixture whose legacy
  heuristic score is 100.0. Do not use prose substrings as concept support.

  `test_conflicts_quality_notes_and_weak_definition_require_review`: assert exact
  finding details/IDs for each discretionary case. Missing optional math alone
  produces no invented hard requirement.

  `test_fingerprints_cover_membership_source_assets_and_pending_journals`:
  parameterize Markdown/metadata edits, add/remove/rename concept, raw/processed/
  archive asset edits, lecture changes, review-file changes, and prepared or
  corrupt persistence journals. Assert stale membership/dependencies differ or
  block, and capture never repairs journals or writes source state.

- [x] **Step 2: Run `pytest tests/test_quality_gate.py -q`; observe intended missing behavior.**
- [x] **Step 3: Implement input capture and policy.** Capture exact bytes before interpretation. Store root-qualified manifest names (`concepts/`, `processed/`, `history/`, `reviews/`, numbered `assets/` roots) and resolved root identities. Discover complete records recursively, reject nested candidate ambiguity and duplicate keys, and use the same records later for refinement. Allow local assets only inside declared concept/history/processed/asset roots; raw PDFs may be byte-hashed when explicitly included as an asset root, never parsed. Include all review-file membership, excluding it from each concept's pre-review fingerprint. Include persistence-journal membership/state bytes in the corpus manifest so a newly pending or changed transaction invalidates a previously passing report; these operational journals do not enter concept review fingerprints.

  Emit hard finding codes for invalid corpus/record/identity/classification,
  definition/provenance/source/asset failures and pending persistence state.
  Match structured source canonical keys or normalized explicit candidate labels
  against concept identity/aliases, verify positive integer page references,
  course association, and every listed lecture hash. Store supported source
  lecture/page tuples in finding/report evidence for review validation.

  Emit `persistence_conflict`, `quality_review`, and `weak_definition` review
  findings; use existing definition-quality cutoff 0.55 only for review routing.
  Readiness never derives pass/fail from aggregate metrics.
- [x] **Step 4: Run `pytest tests/test_quality_gate.py tests/test_concept_document.py tests/test_consolidation.py -q`; require all pass.**
- [x] **Step 5: Inspect diff and run `git diff --check`.** Conditional commit: `feat: capture source-bound publication readiness`.

### Task 3: Resolve Reviews and Persist Verifiable Eligibility Reports

**Files:** Modify `quality_gate.py`, `tests/test_quality_gate.py`, `tests/gate_fixtures.py`.

**Interfaces:**
- Consume Task 2 snapshot, findings, supported-page evidence, and policy versions.
- Produce `evaluate_for_refinement(paths: GatePaths) -> dict`.
- Produce `write_evaluation_report(report: dict, reports_root: Path) -> Path` and `load_evaluation_report(report_path: Path) -> dict`; loader validates artifact schema/identity and is shared by single-page refinement and eligibility validation.
- Produce `require_eligible_report(report_path: Path | None, concepts_root: Path) -> GateSnapshot` and `assert_gate_snapshot_current(snapshot: GateSnapshot) -> None`.

- [x] **Step 1: Add failing review/report tests.**

  `test_review_resolves_only_exact_current_findings`: manually create synthetic
  content-addressed review JSON in test temp root. Require reviewer, valid UTC
  timestamp, rationale, concept key/fingerprint, exact finding ID/content digest,
  allowed disposition, and supporting lecture/page citations. Test partial,
  conflicting, malformed, stale, wrong-concept, and attempted hard-failure override.

  `test_review_history_does_not_self_invalidate`: retain an old valid decision,
  edit draft, and add current decision. Old decision cannot resolve new finding;
  new valid decision can, without deleting history. Report inventory still
  detects review-file edits/additions/removals. No circular dependency on review
  bytes in the fingerprint that the review itself approves.

  `test_pass_and_blocked_reports_are_content_addressed`: pass only with no hard
  or unresolved review findings. Persist both outcomes. Identical input reuses
  exact report without mtime change; differing content at an existing identity
  raises, preserving prior evidence.

  `test_report_validation_rejects_stale_tampered_or_legacy_artifacts`:
  parameterize missing report, metrics-only JSON, altered pass field, wrong policy,
  unknown schema/types, invalid content ID, roots mismatch, missing findings,
  and every Task 2 freshness mutation. Assert rejection without input writes.

- [x] **Step 2: Run `pytest tests/test_quality_gate.py -q`; observe intended new failures.**
- [x] **Step 3: Implement strict artifact schemas and identity checks.** Review payload is schema version 1, concept key/fingerprint, reviewer, `reviewed_at`, rationale, and resolutions containing finding ID/digest, disposition (`accepted_with_evidence` or `not_applicable`), and citations (`lecture_file`, `page_number`). Its `record_id` hashes payload excluding itself; filename must be `<record_id>.json`. Validate all records structurally, retain valid stale records as history, and use only exact-current matches. Contradictory current dispositions block rather than last-write-wins.

  Report includes schema/policy versions, evaluator kind `heuristic_with_source_reference_checks`, roots, manifest/digest, concept fingerprints/support pages, diagnostics, findings/resolutions, review references, eligibility, and `report_id`. ID hashes canonical payload excluding itself; filename is `<report_id>.json`. Write atomically outside draft/refined inputs; never replace different bytes at that identity. Diagnostics retain existing score meaning and do not grant passage.

  Validate report structure, identity, policy, manifest, and derived decision before
  returning evaluated current input bytes. Use recorded roots for source/review
  collection, bind requested concepts root explicitly, and do not rerun technical
  content evaluation inside refinement. Freshness assertion recollects dependency
  identities only; it does not generate approvals or new reports.
- [x] **Step 4: Run `pytest tests/test_quality_gate.py -q`; require green artifact and review tests.**
- [x] **Step 5: Inspect diff and run `git diff --check`.** Conditional commit: `feat: persist and enforce current eligibility evidence`.

### Task 4: Gate and Stage Every Supported Refinement Entry Point

**Files:** Modify `presentation_refinement.py`, `scripts/refine_concepts.py`, `evaluation/evaluate_consolidation.py`, `tests/test_presentation_refinement.py`; create `tests/test_gate_commands.py`.

**Interfaces:**
- Consume Tasks 1-3 parsing, invariants, snapshots, report writer, and eligibility validation.
- Preserve public refinement names with required evidence: `refine_concepts(concepts_root: Path, refined_root: Path, *, evaluation_report: Path | None = None) -> RefinementReport`; `refine_concept_page(concept_dir: Path, refined_root: Path, *, evaluation_report: Path | None = None) -> RefinementResult`. Missing evidence raises GateError before writes.
- Single-page call validates the full report, infers recorded concepts root, and requires concept directory membership in its approved snapshot. It cannot bypass corpus blockers.

- [x] **Step 1: Add failing CLI and publication tests.**

  `test_all_public_entrypoints_block_without_current_pass`: parameterize Python
  batch/single-page and CLI missing/blocked/stale reports. Seed refined sentinels
  and assert byte/mtime/inventory equality after failures, including a last-concept
  failure and no creation of concept output directories.

  `test_approved_refinement_preserves_bytes_and_is_idempotent`: replace old
  ungated fixture with valid synthetic lecture/hash/evaluation. Preserve unknown
  metadata JSON fields exactly, equations/tables/citations, repeated/aliased
  sections, fenced headings, local evidence target bytes, and unrelated refined
  assets. Verify second unchanged run changes no output mtime.

  `test_mutation_during_preparation_blocks_all_publication`: inject source/asset
  edit during preparation and assert stale rejection with all previous output
  untouched. Also reject overlapping roots, reports in input/output, symlinked
  output paths, and corrupted transformation content before final writes.

  `test_evaluation_and_refinement_cli_status`: subprocess valid/blocked evaluation,
  require emitted report path and exit 0/1, then valid/blocked refinement. Missing
  required CLI option returns argparse exit 2. Verify evaluator is not invoked
  after formatting and no production paths are used.

- [x] **Step 2: Run `pytest tests/test_presentation_refinement.py tests/test_gate_commands.py -q`; observe intended missing enforcement.**
- [x] **Step 3: Implement shared enforcement and staging.** Validate all roots and report placement before any output writes. Prepare output from GateSnapshot bytes, preserving each concept's relative directory. Keep raw approved metadata bytes. Use Task 1 formatter/invariant for all Markdown and rebase relative links only where required to preserve the same asset targets, without changing link labels or claims. Stage all requested outputs; recheck snapshot freshness before final publication. Write only changed outputs atomically per file. Do not silently skip incomplete concepts or erase unrelated destination assets. Filesystem failures during final publication raise clearly; no new corpus-wide transaction promise.

  Evaluation CLI adds `--processed`, `--reviews`, repeatable `--asset-root`, and
  `--reports` (default `evaluation/runs/gates`). Print report path, eligibility,
  actionable findings, and diagnostics. Existing `--concepts` remains. Refinement
  CLI adds required `--evaluation`; no force/skip option. Exceptions become
  actionable nonzero JSON results, with no synthetic approval.
- [x] **Step 4: Run `pytest tests/test_concept_document.py tests/test_quality_gate.py tests/test_presentation_refinement.py tests/test_gate_commands.py -q`; require all pass.**
- [x] **Step 5: Inspect diff and run `git diff --check`.** Conditional commit: `feat: gate refinement on exact evaluated inputs`.

### Task 5: Close Repair Publication Bypass and Verify Delivery

**Files:** Modify `scripts/audit_repair_concepts.py`, `tests/test_gate_commands.py`, README, `docs/architecture.md`, `docs/submission_manifest.md`, `evaluation/README.md`, `skills/presentation_refinement/README.md`, `scripts/README.md`, `tests/README.md`, `.gitignore`.

**Interfaces:** Consume existing `write_concept_record` and completed gate/refinement commands. No additional publication or reviewer interface.

- [x] **Step 1: Write `test_repair_apply_changes_only_persistent_drafts`.** Audit-only changes no drafts/refined content; apply archives prior draft bytes through store, advances version once, preserves raw unknown keys in history, and leaves refined bytes/mtimes untouched. Existing evaluation becomes stale. Supplying removed `--refined` option fails clearly rather than retaining hidden writes. Test fixtures use an eligible course and deterministic source-backed repair.
- [x] **Step 2: Run `pytest tests/test_gate_commands.py -q`; observe intended direct-refined-write failure.**
- [x] **Step 3: Make audit/repair draft-only.** Remove `--refined` and all refined writes. Prepare intended draft repairs, update typed metadata, and use `write_concept_record` so prior bytes survive and store owns versions/timestamps. Auditing and reporting remain separate from publication; do not issue reports or approvals on repair's behalf. Preserve remaining source content and persistence conflict traceability.
- [x] **Step 4: Update documentation and exclusions.** Show evaluate -> report review/disposition if needed -> reevaluate -> refine commands, including explicit asset-root examples for local PDF links. Label scores heuristic and formatter a preparation utility; state no new Impeccable adapter. Explain review/report JSON fields, content identities, source-reference limits, stale invalidation, single-writer/partial-I/O limits, and old-command failures. Add `evaluation/reviews/` to local evidence exclusions without deleting files; keep checked-in website bundles functional.
- [x] **Step 5: Run final checks.** `pytest -q -p no:cacheprovider`, `python3 -m compileall -q src/knowledge_review_agent scripts evaluation`, and `git diff --check` must pass. Verify Git status contains only this seam's work plus preexisting persistence changes and image. Do not execute production ingestion, consolidation, evaluation, repair, refinement, or graph rebuild. Complete one fresh-context review of this change, then fix Important/Critical findings with failing tests before final verification. Conditional commit: `fix: keep repairs draft-only and document publication gate`.

## Self-Review and Handoff

- Coverage: shared parsing and preservation (Task 1); exact source-bound inputs
  and policy (Task 2); human dispositions and report identity (Task 3); guarded
  Python/CLI writes and preparation freshness (Task 4); bypass closure,
  persistence compatibility, guidance, and final review (Task 5).
- Each Review Focus condition maps to named tests. Review fingerprints exclude
  their own records; report fingerprints include review inventory, preventing
  self-reference while detecting new conflicting current decisions.
- Hard failures cannot be approved away. Historical valid review records remain
  available but do not count as current approval. Existing metric shapes stay
  diagnostic and unchanged.
- Native implementation complete. One fresh-context review found six Important issues; all fixed in one regression pass. Final suite: 117 passed; compileall and diff checks passed. Changes remain uncommitted under approved sandbox fallback.


## Final review and regression pass

Fresh-context reviewer: `gate_review`; initial verdict request changes, six
Important findings, zero Critical. Fixed with regressions:

1. Reference definitions now share destination discovery/rebasing with inline
   links; balanced parentheses, quoted titles and angle paths retain meaning.
2. Empty normalized aliases and source labels cannot establish page support.
3. Refined destinations cannot overlap retained concept history.
4. Invalid/non-finite metadata and failed diagnostic loads retain blocked reports.
5. Equivalent repeated findings deduplicate by stable identity; duplicate source
   sections remain intact and valid review resolution can pass.
6. Final freshness compares roots, dependency bytes, record/review/journal
   membership and path safety without running content evaluation after formatting.

Ruling: retain approved single-writer/per-file publication scope. Costs: final
filesystem failures can leave partial publication; no corpus transaction or
concurrent-writer guarantee. Reviewer declined full factual certification,
reviewer authentication, prior persistence internals, raw PDF parsing, production
corpus assessment and Impeccable integration, matching approved boundaries.
No Important/Critical findings deferred. No production pipeline commands run.
