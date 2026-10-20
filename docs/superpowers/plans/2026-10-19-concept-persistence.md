# Lossless Concept Persistence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Native execution approved by user on 2026-10-19.

**Goal:** Preserve complete concept evidence and prior versions through duplicate merges, updates, and interrupted writes.

**Architecture:** Deepen the existing file-backed concept store rather than changing storage technology. Consolidation assembles one intended canonical record per affected key; the store owns version allocation, snapshots, recoverable writes, and duplicate retirement. Keep history outside active concept scans.

**Tech Stack:** Existing Python dataclasses, standard-library filesystem/hash/JSON tooling, pytest. No new runtime dependencies.

**Spec:** [Approved persistence spec](../specs/2026-10-19-concept-persistence-design.md)

## Global Constraints

- Keep the existing consolidation command, canonical concept directory layout, lecture artifacts, and draft/refined separation.
- The scope is local, single-writer consolidation. General concurrent writers, network filesystems, and transactional browser reads are not promised.
- For custom roots, use `<concepts-root.parent>/.<concepts-root.name>_history`.
- Do not catch persistence errors and report success. Do not automatically trim history.
- New canonical record starts at version 1.
- Recovering the same operation does not allocate a second version.
- Only affected canonical records are rewritten.
- No raw PDF parsing, ingestion re-run, or modification of raw PDFs.
- No migration or rewrite of local canonical/refined content during development.
- No database, new runtime dependency, or public command replacement.
- Work in current `superpowers-dev` checkout. Preserve untracked `KRA-presentation.png`.
- Git staging previously failed with `Operation not permitted`; keep changes unstaged unless Git access becomes available. No push or merge belongs to this plan.

## Review Focus

1. Journal traversal, symlinks, and unexpected root paths must fail before touching files (Task 2).
2. Unknown JSON keys, partial original records, and binary evidence files must survive byte-for-byte in history (Tasks 1 and 2).
3. Two duplicate directories can contain same relative evidence filename with different bytes; archives and active attribution must keep both (Tasks 2 and 3).
4. An interrupted retirement can leave some originals moved and others active; recovery must finish without overwriting either original or advancing version again (Task 2).
5. A source-hash change with otherwise identical synthesized prose still requires one provenance update; unchanged or absent source mentions must not trigger migration (Task 3).

## File and Interface Map

| File | Responsibility |
| --- | --- |
| `src/knowledge_review_agent/models.py` | Backward-compatible structured persistence-conflict records. |
| `src/knowledge_review_agent/concept_store.py` | Metadata normalization, complete merges, immutable snapshots, versioned record writes, recovery. Keep transaction helpers private here. |
| `src/knowledge_review_agent/consolidation.py` | Assemble one final candidate per key, retain source sections, call store once, recover before discovery. |
| `tests/test_concept_store.py` (new) | Public-store preservation, versions, snapshots, failure/recovery behavior. |
| `tests/test_consolidation.py` | Duplicate, source-retention, incremental, archive-isolation integration checks. |
| `docs/architecture.md`, `docs/knowledge_schema.md` | Describe actual persistence responsibilities and conflict schema. |
| `docs/submission_manifest.md`, `tests/README.md`, `.gitignore` | History exclusions and reproduction/verification guidance. |

Keep existing `load_concept_metadata` and `save_concept_metadata` signatures.
Metadata-only helpers remain compatible with fixtures and refinement; complete
canonical writes go through the new record operation. No whole-repo refactor.

---

### Task 1: Preserve Complete Metadata and Traceable Conflicts

**Files:** Modify `models.py`, `concept_store.py`; create `tests/test_concept_store.py`.

**Interfaces:**
- Produce frozen `PersistenceAlternative(source_record: str, record_sha256: str, value: str, snapshot_id: str = "")`.
- Produce frozen `PersistenceConflict(field_name: str, selected_value: str, alternatives: list[PersistenceAlternative])`.
- Add `ConceptMetadata.persistence_conflicts: list[PersistenceConflict]` with empty default.
- Produce `merge_concept_metadata(concepts_root: Path, records: list[tuple[Path, ConceptMetadata]]) -> ConceptMetadata`; tuple path names original record directory, and conflict paths are stored relative to concepts root.
- Produce `normalize_concept_metadata(metadata: ConceptMetadata) -> ConceptMetadata` and `render_concept_metadata(metadata: ConceptMetadata) -> str` for consistent write bytes.
- Consume existing primary ordering: descending version, timestamp, directory path.

- [x] **Step 1: Add failing public-store tests.**

  `test_merge_preserves_all_metadata_fields`: merge two fixture records with
  distinct text, equations, numeric values, lists, lecture hashes, and explicit
  scope/study priority. Assert primary nonempty scalars stay preferred, empty
  scalars fill from secondary, all lists union deterministically, and primary
  numeric values survive without inferred reset.

  `test_merge_records_conflicting_text_and_hashes`: assert each distinct
  definition/equation/classification/hash alternative contains original path,
  metadata-file SHA-256, and exact field text. Assert selected value matches
  preferred record and conflict ordering is stable. For source hashes use field
  name `source_lecture_hashes.<lecture-reference>`.

  `test_conflict_metadata_roundtrips_and_old_metadata_loads`: assert conflict
  records survive save/load; legacy JSON without the field loads empty list.
  Add an unknown JSON key and verify ordinary reads do not modify source bytes.

- [x] **Step 2: Run `pytest tests/test_concept_store.py -q`; confirm failures describe missing behavior.**
- [x] **Step 3: Implement interfaces in their mapped files.** Normalize all known fields without a second manually maintained subset constructor. Preserve unknown keys in original archived bytes, not by inventing model fields. Merge lists exactly; retain selected numeric/scalar values. Exclude identity/version/timestamp fields from content-conflict flags. Keep distinct source hashes traceable.
- [x] **Step 4: Run `pytest tests/test_concept_store.py tests/test_consolidation.py tests/test_presentation_refinement.py -q`; require all pass.**
- [x] **Step 5: Review task diff and run `git diff --check`.** If Git writes are available, commit only task files as `fix: preserve complete concept merge metadata`; otherwise retain reviewable working-tree changes.

### Task 2: Add Immutable History and Recoverable Complete-Record Writes

**Files:** Modify `concept_store.py`, `tests/test_concept_store.py`.

**Interfaces:**
- Consume Task 1 normalization, rendering, merge, and conflict types.
- Produce `concept_history_root(concepts_root: Path) -> Path`.
- Produce frozen `ConceptWriteResult(changed: bool, metadata: ConceptMetadata, snapshot_id: str, retired_directories: tuple[str, ...])`.
- Produce `write_concept_record(concepts_root: Path, directory: Path, metadata: ConceptMetadata, render_markdown: Callable[[ConceptMetadata], str], *, superseded_directories: tuple[Path, ...] = (), reason: str = "update") -> ConceptWriteResult`.
- Produce `recover_concept_transactions(concepts_root: Path) -> list[str]`, returning recovered transaction identifiers. Corrupt transactions raise `RuntimeError` with retained recovery location.

- [x] **Step 1: Add failing store tests.**

  `test_record_update_archives_original_bytes`: create original Markdown, raw
  JSON with unknown key, binary evidence file, and empty subdirectory. Update
  through public store. Assert snapshot retains complete directory inventory and
  original bytes; live record gets one new version and coherent Markdown/JSON.

  `test_new_record_and_noop_are_stable`: assert new version 1; second identical
  call returns `changed=False` and preserves active bytes, modification times,
  metadata timestamp, version, and history inventory. Renderer includes version
  and timestamp so lifecycle drift cannot hide.

  `test_duplicate_retirement_keeps_both_original_directories`: use same evidence
  filename with different bytes in two directories, plus a partial original
  missing Markdown. Assert all original bytes preserved, one final record, and
  no retirement before live-pair verification.

  `test_interrupted_write_recovers_once`: parameterize failure before archive
  completion, between live replacements, and after first duplicate retirement.
  Inject failure at real filesystem operations, invoke public recovery twice,
  and assert intended live pair, complete originals, stable final version, no
  further changes on second recovery. Pre-journal failure must leave live files
  untouched and permit a normal retry.

  `test_recovery_rejects_unsafe_or_corrupt_state`: parameterize traversal,
  absolute paths outside root, symlinked input, corrupted staged bytes,
  overwritten snapshot, and changed retirement input. Assert failure preserves
  external files, current files, archived bytes, and recovery evidence.

- [x] **Step 2: Run `pytest tests/test_concept_store.py -q`; confirm new tests fail for intended missing behavior.**
- [x] **Step 3: Implement history and transaction protocol.**

  Use `<history-root>/<canonical-id>/<snapshot-id>/manifest.json` and `records/`
  for immutable originals; use `<history-root>/transactions/<transaction-id>/`
  for staged output, retired directories, and journal. Canonical ID combines
  slug with canonical-key hash to prevent slug collisions. Snapshot ID hashes
  canonical key plus sorted original relative paths, inventories, and byte
  hashes. Fill empty conflict-alternative snapshot IDs from verified original
  records before final rendering; retain IDs already referring to older history.
  Transaction ID additionally hashes intended output bytes and retired
  paths. Creation with no originals has no original snapshot; journal still
  retains staged output for recovery.

  Normalize candidate at existing lifecycle values and render once to detect a
  no-op. Only a changed candidate or duplicate retirement allocates version
  `max(original versions) + 1` (or 1 for new record), current UTC timestamp, and
  final render. Caller does not allocate versions. Hashes and journal contain
  final rendered bytes; recovery never invokes renderer or synthesis.

  Archive complete originals using verified copies, staging archives before
  immutable installation. Journal states are `prepared`, `published`, and
  `committed`; never require a state marker to prove a partially completed file
  operation happened. Verify hashes and path existence when resuming. Write
  staged files and journal through same-filesystem temporary files, flush and
  fsync before atomic replacements, and sync parent directories where supported.
  Keep staged output reusable by copying into replacement temporary files.

  After verifying both live hashes, move each redundant directory into retained
  transaction storage. Persist committed state only after retirement completes.
  On errors, propagate failure and retain recovery data. Validate paths and
  original hashes before each destructive replacement/move; reject symlinks.
  No `rmtree` or automatic archive cleanup.

- [x] **Step 4: Run `pytest tests/test_concept_store.py -q`; require all preservation/recovery checks pass.**
- [x] **Step 5: Review task diff and run `git diff --check`.** Conditional commit: `feat: add recoverable concept record persistence`.

### Task 3: Integrate One Lossless Consolidation Commit per Key

**Files:** Modify `consolidation.py`, `tests/test_consolidation.py`.

**Interfaces:**
- Consume Task 1 merge and Task 2 write/recovery interfaces.
- Keep public `consolidate_concepts(processed_root: Path, concepts_root: Path) -> ConsolidationReport` and discovery signatures.
- Add internal `_retain_source_sections(markdown: str, originals: dict[str, str]) -> str` and `_render_persistence_review(markdown: str, metadata: ConceptMetadata) -> str`.

- [x] **Step 1: Add failing consolidation tests.**

  `test_duplicate_merge_preserves_metadata_evidence_and_archives`: exercise
  public consolidation with duplicate records, current mentions, conflicting
  definitions/equations, unique custom sections and identical evidence filenames.
  Assert one active key, complete archived originals, preferred metadata, and
  active evidence attributed to both original records. Assert unresolved field
  alternatives appear as traceable Quality Review flags, not synthesized math.

  `test_no_mentions_preserves_existing_record_exactly`: record with manual
  wording/equation and empty processed root retains exact bytes, times, version;
  report lists it unchanged and no history is created.

  `test_unchanged_sources_do_not_rewrite_records`: consolidate two concepts,
  capture complete active/history inventories, rerun, and assert equality.
  Change one lecture hash while retaining same conceptual prose; assert exactly
  one version increment and snapshot for affected key, unrelated files untouched.

  `test_recovery_precedes_discovery_and_history_stays_invisible`: interrupt a
  public consolidation write, rerun, and assert recovery completes first, final
  version advances once, active discovery/evaluation/graph node counts exclude
  snapshots and retired records. Build graph only in temporary fixture root.

- [x] **Step 2: Run `pytest tests/test_consolidation.py -q`; confirm new tests fail for intended behavior.**
- [x] **Step 3: Integrate store through one assembled candidate per canonical key.** Recover before discovering concepts. Eliminate eager duplicate deletion and separate duplicate-write pass. Merge retained metadata, add current mentions, preserve explicit fields/conflicts, then render and persist once. Store alone allocates final version and timestamp. For existing singleton with no changed lecture hashes, return unchanged rather than migrating its page.

  Retain existing `Slide-derived Evidence`, `Provenance`, and custom sections
  when rebuilding affected pages. Deduplicate retained blocks by normalized
  section name plus exact content digest, keeping all originating record paths
  and hashes. Preserve equations/tables verbatim inside retained evidence;
  conflicting canonical equation alternatives remain in archives and review
  records. Avoid nesting whole previous pages or duplicating retained blocks
  on subsequent updates. Keep learning content before evidence/review metadata.

  Persist conflict alternatives using source path and metadata-byte hash; link
  each to its immutable archive manifest entry after snapshot creation. Preserve
  existing conflict records during later updates. Report retired paths through
  existing `duplicate_dirs` field; add no new CLI arguments.

- [x] **Step 4: Run `pytest tests/test_concept_store.py tests/test_consolidation.py tests/test_graph_builder.py tests/test_presentation_refinement.py -q`; require all pass.**
- [x] **Step 5: Review task diff and run `git diff --check`.** Conditional commit: `fix: consolidate concepts without losing retained evidence`.

### Task 4: Document Persistence Guarantees and Verify Delivery

**Files:** Modify `.gitignore`, `docs/architecture.md`, `docs/knowledge_schema.md`, `docs/submission_manifest.md`, `tests/README.md`.

**Interfaces:** Consume completed store/consolidation behavior; no new runtime interfaces.

- [x] **Step 1: Document actual behavior.** Explain sibling `.concepts_history`, custom-root naming, conflict records, versions, recovery on next consolidation, retained failed journals, and single-writer limits. Clarify two file replacements are recoverable rather than pair-atomic. Explain how recovery errors identify retained artifacts; do not recommend deletion as repair.
- [x] **Step 2: Exclude local history.** Add `knowledge_base/.*_history/` to `.gitignore`; document custom-root history is local state callers must preserve. Verify existing refined pages and graph bundles remain tracked. No generated artifacts are rebuilt.
- [x] **Step 3: Verify public behavior and syntax.** Run `pytest -q -p no:cacheprovider`, `python3 -m compileall -q src/knowledge_review_agent`, and `git diff --check`. Require full suite pass, successful compile, and no whitespace errors. No unconfigured linter/typechecker is claimed as passed.
- [x] **Step 4: Review diff against approved spec.** Check no destructive retirement, lost fields, archived-record discovery, repeated evidence blocks, double version increments, or changes outside selected persistence scope. Inspect `git status --short`; preserve unrelated image and local data.
- [x] **Step 5: Record verification and remaining limits in final response.** Name tests run, preserved guarantees, and single-writer/recovery limits. Conditional documentation commit: `docs: describe lossless concept persistence and recovery`.

## Self-Review and Execution Handoff

- Spec coverage: merge/conflict preservation (Task 1), history and recovery
  (Task 2), current evidence and incremental behavior (Task 3), submission and
  operator guidance (Task 4).
- Each Review Focus item has tests in its owning task. No production corpus
  execution or external-skill run is required.
- Interfaces are defined before consumers; store owns versioning, consolidation
  owns synthesis. Existing public commands remain stable.
- Native execution recommended: tasks share persistence types and transaction
  state closely, so one implementer retains context with less handoff cost.
- Native execution complete. Fresh-context review found three Important issues; each reproduced RED, fixed GREEN, with full suite 31 passed. No deferred minors. Changes remain uncommitted under approved Git sandbox fallback.
