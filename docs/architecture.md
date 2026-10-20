# Architecture

```mermaid
flowchart LR
  A["data/raw lecture PDFs"] --> B["ingest / hash scan"]
  B --> C["data/index.json"]
  C --> D["PDF Parser Skill"]
  D --> E["Concept Filter Skill"]
  E --> F["data/processed/<course>/<lecture>/lecture.md + lecture.json"]
  F --> S["Shared source occurrence index"]
  S --> G["Knowledge Consolidator Skill"]
  G --> H["knowledge_base/concepts"]
  H --> I["Readiness evaluation and heuristic diagnostics"]
  I --> J{"Quality Gate"}
  J -->|current report passes| K["Gated presentation preparation / external Impeccable capability"]
  K --> L["knowledge_base/refined"]
  L --> M["Knowledge Graph Builder Skill"]
  M --> N["knowledge_base/graphs/nodes.json + edges.json + graph.json + state.json"]
  N --> O["Graph Visualization"]
  O --> P["Interactive Website"]
```

## Design choice

- Keep source parsing separate from ingestion state.
- Keep lecture artifacts separate from canonical concept records.
- Keep canonical concept records separate from graph edges.
- Keep provenance attached at every hop.
- Keep ingestion incremental by hash, not by filename.
- Keep consolidation incremental by canonical concept key.
- Keep evaluation ahead of presentation refinement.
- Keep Impeccable as a presentation-only layer.
- Keep refined output separate from draft concept records.
- Keep graph building incremental by canonical concept key and relation fingerprint.
- Keep PDF parsing behind a single adapter until a real importable Anthropic Python API exists.

## Planned shared layer

`src/knowledge_review_agent/` is reserved for shared schema, provenance, and utility code used by all skills.

## Persistent state

- `data/index.json` tracks PDF hashes, status, and output locations.
- `knowledge_base/concepts/<concept>/metadata.json` tracks canonical provenance and versioning.
- `knowledge_base/graphs/` tracks node, edge, state, and delta data.
- `evaluation/` tracks merge-quality checks for concept consolidation.
- `website/` renders refined knowledge for users.

## Lossless concept persistence

`concept_store.py` owns complete canonical-record writes, version allocation,
immutable original snapshots, duplicate retirement, and interrupted-write
recovery. Consolidation assembles one intended record per affected canonical key
and delegates persistence. Existing metadata-only helpers remain available for
fixtures and presentation metadata; they are not a transactional canonical write.

- History lives outside active concept scans at `knowledge_base/.concepts_history/`.
  A custom concepts root uses a sibling named `.<root-name>_history`.
- Snapshots retain complete original directories, including exact Markdown/JSON
  bytes, unknown JSON fields, binary evidence, and empty directories. Manifests
  record paths, hashes, versions, reason, and originating transaction identity.
- Duplicate merges retain preferred nonempty scalar values, fill missing values,
  and union lists. Conflicting text and source hashes remain traceable in
  `persistence_conflicts` and page `Quality Review` notes.
- Active pages retain prior source-evidence, provenance, and custom sections with
  origin attribution, plus unmatched technical sections that existed only in
  Markdown. Literal definitions, intuition, and equations can fill missing
  metadata; conflicting text remains traceable. They do not embed entire earlier
  pages recursively. Relative evidence links are rebased to immutable archive
  files so duplicate filenames cannot substitute another source's bytes.
- A changed canonical record advances its version once. Identical input and
  records without new source contributions leave bytes, versions, and file
  modification times untouched; consolidation is not an implicit page migration.
- Redundant directories move into retained transaction storage only after the
  new Markdown/metadata pair is verified. Originals are never recursively deleted.

Writes are **recoverable, not atomic as a pair**. Each file replacement is atomic;
a process interrupted between replacements can leave mixed live files until
recovery. The next consolidation invocation recovers prepared transactions
before discovering active records, using verified staged bytes without rerunning
synthesis. Recovery does not allocate another version.

Malformed journals, unsafe paths, modified originals, or corrupt snapshots/staged
bytes stop recovery with the retained transaction path in the error. Preserve
that directory and original files for inspection; do not delete a journal as a
repair. No automatic history pruning is provided. Failed pre-journal staging
remains local and does not authorize live writes.
Immutable journal fields must match the transaction-directory digest before
recovery writes; only the recorded transaction state is allowed to advance.

Scope: local single-writer execution. Concurrent writers, network filesystems,
and atomic browser reads across both files are not supported. History is local
durable state and is excluded from GitHub submission, never implicitly deleted.

## Evaluation-to-refinement seam

`quality_gate.py` owns shared discovery, exact input snapshots, source-reference
checks, discretionary review resolution, and immutable eligibility reports.
`concept_document.py` supplies fence-aware parsing and preservation checks used
by both gate and formatter. Existing aggregate evaluation metrics remain
diagnostics; scores never grant publication or override missing evidence.

Evaluation captures draft membership/bytes, contributing lecture hashes and
supported concept/page/course references, linked local assets, review history,
persistence journals, resolved roots, and policy/schema versions. Concept review
fingerprints exclude reviews; corpus/report identities include review inventory.
This avoids circular approval hashes while invalidating stale reports.

Hard failures cannot be overridden. Discretionary quality notes, persistence
conflicts, and weak-definition findings require exact-current, evidence-backed
human dispositions. The system never creates approvals. Reports and reviewer
records are local trusted evidence, not authenticated signatures or a complete
factual-accuracy certificate.

Both public Python refinement functions and the CLI require a passing report.
All requested output is prepared from evaluated bytes, preserving metadata JSON
exactly and keeping technical section content. Link rebasing preserves original
asset targets. Inputs are rechecked before changed files are published; no
content evaluator runs after formatting. Eligibility, preservation, or freshness
failure leaves refined output untouched.

Audit/repair applies changes to persistent drafts only. It cannot patch refined
pages; repaired drafts invalidate older evaluation. Website viewing remains
independent of evaluation and local source data.

Scope remains local single-writer use. Final output file replacements are atomic
individually, not as a corpus transaction; a filesystem error during publication
is reported and may leave partial updates. Existing deterministic formatting is
a preparation utility, not a new Impeccable integration.

## Shared source occurrences

`source_occurrences.py` builds one in-memory index of existing lecture JSON per
command. It retains exact bytes/hashes, immutable structured/candidate/text-line
locations and source issues. Consolidation adapts occurrences into selected
mentions; audit ranks text evidence and groups display wording; gate requires
explicit bounded page support. Those consumer policies remain distinct.

Before, all three paths walked source pages independently. Now source identity,
course-ID/name fallback, source declarations and page inventory validation share
one module. Audit repair is restricted to declared lecture paths and hashes.
Repeated text can share a display group while every original citation survives.
No index is persisted, no PDF is reprocessed and no canonical metadata migration
runs. Final publication freshness checks hashes/membership without source parsing.

## Graph presentation contract

`graph_bundle.py` owns explicit site/input paths, refined snapshots, versioned
presentation validation and atomic graph.json publication. Internal topology and
state/deltas remain in graph_builder/graph_store. Refined metadata must match node
identity/version/classification/ranks/contributions before export; drafts never
supply hidden enrichment. Shared Markdown parser retains fenced and duplicate
section content. Browser graph-contract.mjs checks shape, endpoints, statistics
and published URLs before app/Cytoscape state; it never rebuilds missing data.

New exports use schema 2; checked schema-1 adapter preserves existing static site
without regeneration. No-op export preserves old timestamp/bytes/mtime. Changed
export uses atomic per-file replace; internal graph state can advance before a
presentation mismatch rejects. No whole-site transaction/concurrency guarantee.
