# Lossless concept persistence

Status: approved and implemented on 2026-10-19; verified with 31 passing tests and fresh-context review fixes.

## Intent and acceptance

The selected architecture-review candidate is persistent concept records.
Consolidation must preserve source evidence, complete metadata, and previous
versions while merging duplicate canonical keys. A failed or interrupted write
must leave enough durable state to recover without guessing or deleting evidence.

Keep the existing consolidation command, canonical concept directory layout,
lecture artifacts, and draft/refined separation. Success means duplicate merges
retain all contributions, updates preserve prior bytes, reruns are stable, and
archive records never become active concepts or graph nodes.

## Observed failure

- `consolidation._merge_existing_records` reconstructs only part of
  `ConceptMetadata`. Definitions, classification, applications, equations, and
  other fields can disappear.
- Duplicate directories are permanently removed before the merged record is
  written.
- `_write_concept_record` replaces Markdown and metadata separately, without a
  durable previous version or recovery record.
- Records without current lecture mentions are regenerated from metadata. That
  can replace retained source detail with generic synthesis.
- Concept discovery recursively scans `metadata.json`; storing history inside
  the active concept root would turn historical versions into duplicates.

## Alternatives

1. **Recommended: deepen the existing file-backed concept store.** Keep existing
   readers and paths; add lossless merge policy, immutable snapshots, and
   recoverable record writes. Smallest migration cost and direct leverage over
   the observed failures.
2. **Patch consolidation only.** Preserve more fields and replace deletion with
   copies. Less code initially, but persistence policy stays scattered and
   two-file writes remain vulnerable to interruption.
3. **Move canonical state into a database.** Transactions become stronger, but
   adds state migration, tooling, and export obligations unrelated to the current
   failure. Defer until real concurrency or scale requires it.

## Module responsibilities

- `concept_store.py`: canonical metadata normalization, complete-record
  persistence, immutable history, duplicate retirement, and recovery mechanics.
  Retain existing metadata read/write helpers for existing callers.
- `consolidation.py`: determine canonical keys, assemble source mentions, choose
  preferred current values, synthesize new content, and report changes. Delegate
  durable writes and retirement to the store.
- `models.py`: compatible additions for traceable persistence conflicts, if
  needed. Older metadata must continue to load with defaults.
- Existing discovery and evaluation callers continue to see active concept
  records only. Graph construction and publication policy are outside this change.

Keep cohesive persistence logic together. Do not split transaction steps into
single-use pass-through modules or introduce a generic storage framework.

## Merge policy

1. Select the existing primary record using the current deterministic order:
   highest version, latest timestamp, then directory path. Retain its directory,
   canonical identity, and nonempty preferred scalar values.
2. Fill empty scalar fields from other contributing records in that same order.
   Preserve explicit scope and study-priority values instead of re-inferring them.
3. Union list-valued contributions deterministically. Deduplicate exact values
   without treating different equations or evidence passages as equivalent.
4. Preserve all source lecture references and hashes. When the same lecture
   reference has conflicting hashes, retain the primary current association and
   record all alternatives with their originating records for review.
5. Preserve distinct definitions, equations, or classification alternatives in
   traceable conflict records. Keep the preferred current value active; do not
   concatenate competing mathematical claims into a synthetic statement.
6. Expose unresolved content conflicts under `Quality Review`, following the
   existing page schema. Each flag identifies its field and archived source
   record. Identical reruns must not duplicate flags.
7. Retain original Markdown and JSON byte-for-byte in history, including unknown
   JSON fields and custom page sections. Keep unique source evidence and its
   attribution available from the active canonical page when duplicates merge.
   Archiving alone must not erase source contributions from the current record.
8. Records with no new source contribution stay untouched. Do not use a routine
   consolidation run as an implicit legacy-page migration.

No new factual claims, mathematical corrections, or automatic semantic conflict
resolution are part of persistence.

## History and traceability

History lives in a sibling directory derived from the active concepts root:

```text
knowledge_base/concepts/<concept>/concept.md
knowledge_base/concepts/<concept>/metadata.json
knowledge_base/.concepts_history/<canonical-id>/<snapshot-id>/manifest.json
knowledge_base/.concepts_history/<canonical-id>/<snapshot-id>/records/...
```

For custom roots, use `<concepts-root.parent>/.<concepts-root.name>_history`.
The default therefore resolves to `knowledge_base/.concepts_history`.

Snapshot identifiers derive from canonical identity plus sorted contributing
record paths and byte hashes, rather than timestamps alone. Reusing an existing
snapshot requires verifying matching bytes. Never replace differing historical
content. Manifests record schema version, original paths, byte hashes, concept
versions, operation reason, and transaction identity.

Archives preserve each complete original directory, including extra evidence
files, before retirement. They are local durable state, excluded from GitHub
submission and active concept discovery. Exclusion never authorizes deletion.

## Write and recovery protocol

The scope is local, single-writer consolidation. General concurrent writers,
network filesystems, and transactional browser reads are not promised.

1. Recover any pending transaction for the target record before preparing a new
   one. Verify journal paths stay within the active root and its derived history
   root. Reject malformed or unverifiable recovery state without deleting it.
2. Compute intended output entirely before changing live files. If current bytes
   already match, return unchanged without advancing versions or timestamps,
   creating history, or touching file modification times.
3. Snapshot all original records and verify archive bytes before replacing or
   retiring anything. Failure here leaves every active record untouched.
4. Stage the complete new Markdown/metadata pair with hashes. Persist recovery
   journal before replacing live files. Journal records intended output and
   original snapshots; recovery does not re-run synthesis.
5. Replace each live file atomically using same-filesystem staging. Flush staged
   files before replacement. Two independent file replacements are not claimed
   to form one atomic transaction.
6. Verify the final live pair against staged hashes. Only then retire duplicate
   directories by moving them into retained transaction storage, never by
   permanent recursive deletion.
7. Mark transaction committed after all intended live writes and retirements
   succeed. Leave interrupted transaction state available for deterministic
   recovery on the next consolidation invocation.
8. Recovery rolls forward to the journaled output and completes remaining
   retirements idempotently. If required staged data is unavailable or hashes
   differ, fail with actionable recovery paths and keep originals/archives.

Do not catch persistence errors and report success. Do not automatically trim
history. Every operation must be restartable at its journaled phase.

## Versions and incremental behavior

- New canonical record starts at version 1.
- A duplicate merge that changes active content advances from the maximum
  contributing version exactly once for the committed result.
- Each later content-changing update advances the active version once and
  preserves its previous complete record.
- A no-op changes no active bytes, timestamps, versions, or history.
- Recovering the same operation does not allocate a second version.
- Only affected canonical records are rewritten. Existing source-evidence
  sections must not disappear when current lecture mentions are missing.

## Scope exclusions

- No raw PDF parsing, ingestion re-run, or modification of raw PDFs.
- No migration or rewrite of local canonical/refined content during development.
- No quality-gate, evaluator-score, graph-alias, or website-fallback fixes.
- No presentation refinement, graph rebuild, reviewer interface, or archive
  garbage collection.
- No database, new runtime dependency, or public command replacement.

## Verification requirements

Regression checks exercise the public consolidation/store seam with synthetic
records in temporary directories:

- Merge duplicate records containing distinct definitions, equations,
  classification, numeric fields, lists, hashes, custom sections, and evidence.
  Assert preferred active values, retained alternatives, and complete archives.
- Preserve exact original bytes, unknown JSON keys, and extra evidence files.
- Update an existing canonical record; confirm complete prior version retained.
- Run unchanged input twice; assert identical active bytes, versions, file
  modification times, and archive inventory.
- Leave records with no current lecture mentions untouched.
- Inject failure before snapshot completion, between live file replacements,
  and during duplicate retirement. Rerun recovery and verify complete intended
  output, retained originals, and no duplicate version increments.
- Reject corrupt staged data or unsafe journal paths without destructive repair.
- Ensure history does not affect consolidation discovery, graph nodes, or
  evaluation concept counts.
- Keep all existing tests passing. Run relevant tests after each tracer slice,
  then the full suite and whitespace checks before reporting implementation done.

Tests must verify observable preservation and recovery behavior rather than
private helper call order. Do not run production consolidation as a test.

## Documentation and delivery

Implementation should update architecture/schema documentation, submission
exclusions, and test guidance to describe actual behavior and recovery limits.
Keep work in the current `superpowers-dev` checkout unless the user requests
isolation. Preserve existing untracked `KRA-presentation.png`.

Implementation completed through the approved native plan. Runtime changes stay
uncommitted because Git staging is sandbox-blocked. No local corpus migration,
PDF parsing, presentation refinement, or production graph rebuild was performed.
