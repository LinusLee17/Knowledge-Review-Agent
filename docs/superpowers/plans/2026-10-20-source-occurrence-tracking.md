# Source Occurrence Tracking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking. Preserve user's native execution preference: parent implements tasks; one fresh-context final reviewer checks complete change.

**Goal:** Share source occurrence identity and lookup across consolidation, audit/repair and evaluation while preserving every citation and blocking repairs from undeclared or changed lecture sources.

**Architecture:** One in-memory index owns validated lecture bytes, immutable occurrences and scoped queries. Consolidation retains selection/synthesis, audit retains scoring/display grouping, gate retains strict eligibility policy. Existing persistence and dependency-only final freshness remain authoritative.

**Tech Stack:** Existing Python, standard-library dataclasses/JSON/SHA-256/path tooling, pytest. No new dependency or durable state.

**Spec:** [Approved source occurrence design](../specs/2026-10-20-source-occurrence-tracking-design.md), approved 2026-10-20.

## Global Constraints

- Preserve completed persistence and evaluation/refinement changes on current `superpowers-dev` checkout.
- No production ingestion, consolidation, audit/repair, evaluation, refinement or graph builds during implementation.
- No raw PDF parsing, mutation or unchanged-PDF reprocessing.
- No new database, CSV state, global cache or generated submission bundle.
- Legacy concept metadata remains loadable without occurrence fields.
- No canonical/refined page migration; no graph or website changes.
- No external network lookup, LLM extraction, quiz or interview features.
- Existing complete canonical snapshots/provenance remain intact.
- Final prepublication check remains dependency-only: hashes, roots, membership and path safety. Never rebuild occurrence index or rerun content policy after formatting.
- Use synthetic temporary lecture JSON and canonical-record fixtures only.
- Preserve unrelated `KRA-presentation.png` and all prior uncommitted work. Reuse existing approved sandbox fallback: uncommitted reviewable files, no staging, push, merge or new worktree.
- Each task follows RED -> GREEN. Native parent implementation, one fresh-context final review, one regression-fix pass for Important/Critical findings, then full verification.

## Review Focus

1. Identical wording from different courses/pages, or repeated entries on one page, must retain every locator even when only one display group fits limit (Tasks 1/3).
2. Conflicting canonical keys, blank aliases, course-name fallback and text-only matches must not falsely establish structured page support (Tasks 1/4).
3. Duplicate JSON keys, invalid source declarations, non-finite values and bad page inventories must produce source issues before draft writes, never silent omissions or unsavable reports (Tasks 1/2/4).
4. Course-wide discovery must never authorize repair using another lecture, changed hash or empty scope; unrelated bad lectures must not block a valid explicitly scoped repair (Task 3).
5. Shared lectures must be read/parsed once per command; occurrence objects must resist caller mutation; no new source parsing may run after formatting starts (Tasks 1/3/4/5).

## File Map

| File | Responsibility |
| --- | --- |
| `src/knowledge_review_agent/source_occurrences.py` (new) | Exact source bytes, validation, immutable occurrence identities, deterministic discovery/queries and explicit source issues. |
| `src/knowledge_review_agent/consolidation.py` | Compatibility wrappers and occurrence-to-mention adaptation; keep educational selection/rendering and record store unchanged. |
| `src/knowledge_review_agent/concept_quality.py` | Ranked display evidence with complete grouped citations; compatibility collector delegates to shared index. |
| `scripts/audit_repair_concepts.py` | Reuse one index; report coverage/issues; enforce declared source scope before draft repair. |
| `scripts/consolidate_knowledge.py` | Structured nonzero error for invalid source corpus. |
| `src/knowledge_review_agent/quality_gate.py` | Build shared source index from captured bytes; retain hashes, strict support and report flow; gate policy `2`. |
| `tests/source_fixtures.py` (new) | Synthetic exact-byte lectures and canonical fixtures shared by new source tests. |
| `tests/test_source_occurrences.py`, `tests/test_concept_quality.py` (new) | Public index/grouping/scope contracts. |
| Existing consolidation/gate/command/refinement tests | Cross-consumer, persistence, CLI and phase-order regressions. |
| README, architecture/schema/evaluation/script/test docs | Describe identities, grouped coverage, source scope, compatibility and reevaluation. |

## Shared Contracts

All new source types live in `source_occurrences.py`, without importing gate, consolidation or concept quality. Use existing `normalize_concept_key`. Policy `SOURCE_OCCURRENCE_POLICY_VERSION = "1"` is distinct from gate policy.

```python
@dataclass(frozen=True)
class SourceIssue:
    lecture_file: str
    code: str
    locator: str
    message: str

@dataclass(frozen=True)
class SourceRecord:
    relative_path: str
    sha256: str
    raw: bytes
    course_id: str
    course_name: str
    source_pdf: str
    page_count: int
    payload: Mapping[str, object]  # recursively read-only; arrays become tuples

@dataclass(frozen=True)
class SourceOccurrence:
    occurrence_id: str
    source: SourceRecord
    page_number: int
    json_pointer: str
    kind: str  # structured, candidate, text_line
    labels: tuple[str, ...]
    canonical_key: str
    identities: tuple[str, ...]
    text: str
    page_heading: str
    line_number: int = 0
    start: int = 0
    end: int = 0
    item: Mapping[str, object] = ...  # read-only structured fields; empty otherwise

@dataclass(frozen=True)
class SourceMatches:
    occurrences: tuple[SourceOccurrence, ...]
    issues: tuple[SourceIssue, ...]

@dataclass(frozen=True)
class SourceIndex:
    records: tuple[SourceRecord, ...]
    occurrences: tuple[SourceOccurrence, ...]
    issues: tuple[SourceIssue, ...]

    def find(self, concept_name: str, aliases: Iterable[str] = (), *,
             lecture_hashes: Mapping[str, str] | None = None,
             allowed_courses: AbstractSet[str] | None = None,
             kinds: tuple[str, ...] = ("structured", "candidate"),
             text_search: bool = False) -> SourceMatches: ...

def index_sources(sources: Iterable[tuple[str, bytes]]) -> SourceIndex: ...
def load_source_index(processed_root: Path) -> SourceIndex: ...
```

`Mapping`, `Iterable` and `AbstractSet` use `collections.abc`. Empty immutable mappings use a dataclass factory; do not share mutable defaults. Source course identity = nonempty `course_id` else `course_name`.

**Locator/identity:** pointer is `/pages/<array-index>/concepts/<item-index>`, `/pages/<array-index>/concept_candidates/<candidate-index>`, or `/pages/<array-index>/extracted_text`. Text lines add 1-based line number and zero-based `[start,end)` character offsets excluding line terminator, relative to decoded extracted text; preserve whitespace/CRLF in `text`. Structured `text` is exact `evidence` or empty, not generated context. Candidate `text` is exact label. Occurrence ID hashes canonical ASCII JSON (`sort_keys=True`, compact separators, `allow_nan=False`) containing `policy`, `lecture_file`, `lecture_sha256`, `pointer`, `line_number`, `start`, `end`. Do not import gate digest helper and create a cycle.

**Query:** normalize nonempty query name/aliases. For structured/candidate identity match, explicit normalized `canonical_key` is authoritative when present; otherwise intersect normalized original labels/aliases. A matching display name cannot override an unrelated explicit key. `text_search=True` requires `kinds=("text_line",)` and uses normalized phrase matching for discovery; raw text remains exact, audit retains short-alias/quality filtering. Invalid mode raises `ValueError`.

**Scope:** `lecture_hashes=None` means discovery across loaded records; `{}` means no declared sources, returns `missing_source_scope`, never expands to discovery. Supplied entries require safe relative path, lowercase 64-hex SHA-256, matching bytes and allowed course membership. Return explicit `missing_source`, `invalid_source_hash`, `source_hash_mismatch` or `source_course_mismatch` as appropriate. Invalid declared sources produce issues, not usable matches. Query issues include source validation issues only within explicit lecture scope; discovery returns all source issues because malformed course identity cannot be safely filtered. Empty/invalid query identity returns no matches.

**Order/validation:** records sort by relative path; occurrences by relative path/page/pointer/line offsets; issues by lecture/code/locator/message. Duplicate identical input paths/bytes coalesce; conflicting bytes for same relative path yield `duplicate_source` and no usable record. Recursively freeze parsed values, retaining raw bytes. Reject malformed/non-finite JSON and duplicate object keys; validate object/list/string/numeric fields consumed by all three consumers. Validate real positive integer page count, unique real positive page numbers <= count, structured label variants and item aliases, optional source object, and exact enclosing page/PDF agreement if item source fields supplied. Missing optional text/heading/lists default empty. Nonempty malformed fields produce issues; reject affected lecture from usable records rather than partially trusting it. Do not require all declared pages to be present when absent pages are not claimed as support. No guessed page numbers.

**Filesystem:** loader discovers lecture JSON, rejects symlink files/directories and unsafe relative source paths, reads each source once and passes same bytes to indexer. Read failures become issues. Absent processed root remains empty index for existing duplicate-only consolidation workflows; explicit requested missing lectures still fail queries. No filesystem checks in `index_sources`; gate supplies bytes already checked by manifest reader. Raw PDFs are never opened.

---

### Task 1: Validated Source Index and Occurrence Queries

**Files:** Create `source_occurrences.py`, `tests/source_fixtures.py`, `tests/test_source_occurrences.py`.

**Interfaces:** Produce all Shared Contracts above. Fixtures expose `lecture_bytes(*, pages: list[dict], course_id: str = "C1", course_name: str = "", pdf: str = "C1/L1.pdf", page_count: int | None = None) -> bytes`, filling default count from fixture pages, never from production invalid input.

- [x] **Step 1: Write failing public-contract tests.**
  - `test_occurrence_identity_and_raw_text`: JSON with structured evidence, candidate and `"  x = 1\r\nnext"`; assert ID is 64 hex, raw text/offset slice exact, key labels preserved; nested `record.payload`/`occurrence.item` mutation fails without changing later query.
  - `test_order_hash_changes_and_duplicate_locations`: reversed source input gives same tuples; changed bytes change IDs; identical text in two lectures and two entries on same page yields distinct locators/IDs. Duplicate identical path coalesces; conflicting bytes produce issue and no record.
  - `test_explicit_keys_aliases_and_text_search`: unrelated explicit key blocks matching display name; key/accepted alias/candidate matches succeed; punctuation-only aliases fail; raw substring search returns text lines only and cannot satisfy default identity query. Parametrize all four structured label spellings.
  - `test_invalid_source_is_reportable`: malformed/array/non-finite/duplicate-key JSON, bad page count/duplicate/missing/out-of-range/bool/string page, invalid course/lists/items/aliases/source declarations produce stable issues and zero usable records from that lecture. Valid course-name fallback, missing optional fields and partial page inventory succeed.
  - `test_scope_is_explicit`: empty mapping, missing lecture, wrong/malformed hash and wrong course produce named issues; valid restricted query excludes unrelated lecture/issues. Returned locations match exact expected source/page/pointer.
  - `test_loader_reads_exact_bytes_once_and_rejects_symlinks`: count `Path.read_bytes` for temp lectures, assert hashes equal those bytes; symlink root/file/directory and `../`/absolute supplied paths yield issues. Missing processed root yields empty index; no outputs written.

  Minimal contract assertions (using new fixture):

  ```python
  raw = lecture_bytes(pages=[{"page_number": 1, "concept_candidates": ["Linear Regression"]}])
  first = index_sources([("C1/L1/lecture.json", raw)])
  second = index_sources([("C1/L1/lecture.json", raw)])
  assert first.occurrences == second.occurrences
  assert len(first.find("Linear Regression").occurrences) == 1
  assert first.find("Linear Regression", lecture_hashes={}).issues[0].code == "missing_source_scope"
  ```

- [x] **Step 2: Run RED.** `pytest tests/test_source_occurrences.py -q -p no:cacheprovider` must fail for missing module/contracts; resolve fixture mistakes before treating failure as intended.
- [x] **Step 3: Implement shared module.** Implement signatures, deterministic IDs, frozen values, validation, issue propagation and exact/scoped queries from Shared Contracts. Keep source parsing local and independent of consumer policies. No profile enrichment or content synthesis.
- [x] **Step 4: Run GREEN.** Same command passes. `python3 -m compileall -q src/knowledge_review_agent/source_occurrences.py` succeeds.
- [x] **Step 5: Record checkpoint.** Ledger records RED/GREEN and source schema decisions. Conditional commit if Git becomes writable: `feat: add shared source occurrence index`; otherwise retain approved uncommitted fallback.

### Task 2: Consolidation Uses Validated Occurrences

**Files:** Modify `consolidation.py`, `scripts/consolidate_knowledge.py`, `tests/test_consolidation.py`; use new source fixtures.

**Interfaces:** Consume `load_source_index`, `index_sources`, `SourceIndex` and `SourceOccurrence`. Produce `SourceValidationError(ValueError)` in `source_occurrences.py`, initialized with `issues: tuple[SourceIssue, ...]` and a deterministic readable message. Preserve `LectureArtifact(path, relative_path, sha256, payload)` constructor plus optional trailing `source_index: SourceIndex | None = None`; preserve `discover_lecture_artifacts(processed_root)`, `build_mentions(artifact)` and `collect_mentions(artifacts)` return shapes. Add trailing `ConceptMention.occurrence_ids: tuple[str, ...] = ()`.

- [x] **Step 1: Write failing integration tests.**
  - `test_mentions_retain_occurrences_without_changing_selection`: structured pages suppress candidate-only fallback as before; candidate-only page still uses profiles/importance rules. Selected mentions' IDs resolve into source index; duplicates previously collapsed in mention selection retain all contributing occurrence IDs. Source occurrence count remains separate from existing `total_mentions`.
  - `test_source_validation_precedes_canonical_writes`: mix valid lecture/new concept with malformed second lecture; assert exception includes source issues and inventory of active/history roots stays unchanged. CLI returns 1 with JSON error/issues, no traceback or draft writes.
  - `test_consolidation_loads_shared_lectures_once`: count exact-byte reads, build multiple concepts, assert one read per lecture including hashing. Compare existing provenance/selection assertions and source raw data unchanged.
  - Retain existing `test_unchanged_sources_do_not_rewrite_records`, affected-key update, duplicate retirement, archived asset, absent-source and recovery regressions without weakening assertions.

- [x] **Step 2: Run RED.** `pytest tests/test_consolidation.py -q -p no:cacheprovider` exposes missing occurrence IDs and missing validation-before-write behavior.
- [x] **Step 3: Adapt consolidation.** Discover/index once before new canonical writes or recovery mutation; abort on source issues with `SourceValidationError` carrying source issues (defined in source module). Recovery still precedes discovery of active concept records. Compatibility artifacts share same index and copied decoded payload from indexed bytes; standalone legacy `build_mentions` indexes exact `artifact.path` bytes if no index supplied, checking supplied SHA. Adapt structured occurrences into existing `_normalise_concept_source`; use candidate occurrences only on pages with no structured concepts in source. Keep source labels/raw text distinct from synthesized fields. Retain existing normalization, scoring, dedupe and profiles; combine IDs when mention dedupe occurs. CLI catches this error and prints structured stderr JSON with exit 1.
- [x] **Step 4: Run GREEN.** `pytest tests/test_source_occurrences.py tests/test_consolidation.py tests/test_concept_store.py -q -p no:cacheprovider` passes. No production command executed.
- [x] **Step 5: Record checkpoint.** Note wrapper compatibility/no-op evidence in ledger; conditional commit `refactor: build consolidation mentions from source occurrences` under same fallback.

### Task 3: Audit Coverage and Declared-Source Repair Scope

**Files:** Modify `concept_quality.py`, `scripts/audit_repair_concepts.py`, `tests/test_gate_commands.py`; create `tests/test_concept_quality.py`.

**Interfaces:** Keep first four `SourceEvidence(course_id, lecture_file, page_number, text)` fields; add `occurrences: tuple[SourceOccurrence, ...] = ()`. Add frozen `SourceEvidenceSelection(evidence: tuple[SourceEvidence, ...], coverage: tuple[SourceOccurrence, ...], issues: tuple[SourceIssue, ...])` and `select_source_evidence(index: SourceIndex, concept_name: str, aliases: list[str], allowed_courses: set[str], limit: int = 8, *, lecture_hashes: Mapping[str, str] | None = None) -> SourceEvidenceSelection`. Existing `collect_source_evidence(processed_root, concept_name, aliases, allowed_courses, limit=8, *, source_index: SourceIndex | None = None, lecture_hashes: Mapping[str, str] | None = None) -> list[SourceEvidence]` wraps selection; if issues present raise `SourceValidationError`, never hide incomplete search. `limit=0` returns zero display groups with full coverage; negative limit raises `ValueError`.

- [x] **Step 1: Write failing evidence/command tests.**
  - `test_grouped_evidence_preserves_all_locations`: same cleaned text on two courses/pages forms one group with all occurrence references; retain ranking tie-break order. Limit 1 caps groups only, full accepted-match coverage includes lower ranked groups; limit 0 retains coverage; negative rejects. Each raw locator reconstructs original text. `QualityFinding.to_dict()` then `json.dumps` must succeed without bytes, mapping proxies or whole lecture payloads in output.
  - `test_compatibility_collector_reuses_index`: existing positional API returns list/primary citation fields; supplied index triggers no source reads. Source issues raise explicit error; discovery never mutates canonical files.
  - `test_repair_rejects_undeclared_or_changed_sources`: parameterize missing hash, mismatched hash, empty contributing lectures, wrong course, unsupported page, evidence in unrelated same-course lecture only and empty evidence. Force otherwise repairable draft; `--apply` leaves draft/refined/history inventory unchanged and report contains blocked reason. Named-rule/section-only repair cannot bypass scope.
  - `test_explicit_scope_ignores_unrelated_invalid_lecture`: malformed non-contributor is reported at corpus level but valid contributor still permits source-backed repair. Malformed contributor blocks that concept.
  - `test_audit_builds_index_once_for_multiple_concepts`: invoke CLI adapter in-process over temp roots, count lecture reads and index construction; assert one each per run. Audit-only changes no draft files. Preserve existing valid apply test for exact prior-byte archive, single version advance, stale prior report and untouched refined sentinel.

- [x] **Step 2: Run RED.** `pytest tests/test_concept_quality.py tests/test_gate_commands.py -q -p no:cacheprovider` exposes citation loss, repeated reads and undeclared-source writes.
- [x] **Step 3: Implement grouped selection and scoped command.** Query raw text occurrences using existing audit filters/scoring; coverage is all accepted raw occurrences before display cap. Group by existing normalized lowercase cleaned text without dropping source locations. `SourceEvidence` primary citation is deterministic first ranked location, not an invented combined page. Command builds index once, includes metadata canonical key alongside query name/aliases, uses exact contributing lecture/hash map (missing entries must stay explicit invalid entries, not disappear), existing course exclusions and shared identity lookup to require page support. Skip entire affected repair when source issues, missing contributor support or no usable text evidence; record `repair_blocked` plus source issues. Do not set quality score or write sections on blocked path. Keep generation/ranking heuristics unchanged otherwise. Add report fields `source_issues` at corpus level and per finding `source_coverage`, `source_issues`, `repair_blocked`; serialize compact occurrence references only (ID, lecture/hash, course, PDF, page, pointer/offsets, raw text), never embed entire source payload/raw bytes. Replace recursive `asdict` in `QualityFinding.to_dict()` with explicit field/evidence/reference serialization, keeping existing public result fields. Keep existing `findings`, `repaired`, `excluded_courses`, `apply` and primary evidence fields. Persist audit report before returning exit 1 if any attempted repair blocked, else existing 0; audit-only returns 1 for relevant invalid source input but normal quality flags remain report data.
- [x] **Step 4: Run GREEN.** Same targeted command passes, including existing removed-`--refined`/draft-only regression. Verify no new approvals or lecture provenance invented.
- [x] **Step 5: Record checkpoint.** Log scope/exit semantics and read-count evidence; conditional commit `fix: retain audit citations and enforce repair source scope` under same fallback.

### Task 4: Gate Uses Captured Source Index

**Files:** Modify `quality_gate.py`, `tests/test_quality_gate.py`, `tests/test_presentation_refinement.py`, `tests/test_gate_commands.py`; extend synthetic fixtures only where needed.

**Interfaces:** Consume Task 1 `index_sources` and scoped `SourceIndex.find`. Keep all public `GatePaths`, report/citation shapes and refinement entry points. Set `GATE_POLICY_VERSION = "2"`; keep `GATE_SCHEMA_VERSION = 1` because serialized shape unchanged. Extend `GateConcept` with optional trailing `source_occurrence_ids: tuple[str, ...] = ()` for in-process traceability; do not alter serialized supported-page tuples or reviewed citation schema.

- [x] **Step 1: Write failing gate/ordering tests.**
  - `test_gate_shared_identity_and_unique_page_support`: all structured label variants, candidate labels, source alias and course-name fallback work; repeated occurrences collapse to unique page tuples while IDs remain traceable to index. For each selected occurrence ID, independently index same source bytes and verify same locator/ID. Selection sets may differ across consumers/kinds; do not require text-line IDs to equal structured IDs.
  - `test_explicit_key_conflict_and_text_only_do_not_pass`: matching display name with unrelated key, blank aliases or text-only mention cannot establish structured support. Valid alias/key query still works.
  - `test_gate_persists_blocked_source_issues`: duplicate/missing/bool/string/out-of-range page, malformed lecture, unsafe references and source page/PDF conflicts yield hard source findings and savable blocked report; inputs untouched. Relevant malformed source cannot disappear, unrelated unreferenced source remains outside gate corpus.
  - `test_previous_gate_policy_requires_reevaluation`: construct correctly content-addressed policy-1 report; load/refinement rejects unsupported policy before output writes. Current-policy pass/report/review flow still works; no conversion/approval generated.
  - Extend `test_no_quality_scoring_after_formatting`: instrument both shared index constructor and definition evaluator; neither may run after formatter. Keep mutation and membership freshness cases intact. Shared source used by multiple concepts is read and indexed once; gate must not invoke filesystem source loader or reopen lecture outside manifest reader.

- [x] **Step 2: Run RED.** `pytest tests/test_quality_gate.py tests/test_presentation_refinement.py -q -p no:cacheprovider` exposes independent matching, old policy acceptance or missing IDs/validation.
- [x] **Step 3: Integrate shared index in snapshot capture.** Use two capture phases: capture draft bytes/metadata and collect declared references; read distinct safe source paths through existing manifest reader; build one index from successful exact bytes. Then evaluate each concept with scoped matches using metadata canonical key, name and aliases as query identities, wiring cached manifest digests into its dependencies, including shared sources. Missing/unreadable paths remain manifest evidence and source findings. Translate source issues into hard findings; retain weak-definition/review policy, assets, journals and review fingerprints. Require support in every contributing lecture and course. Keep unique sorted `(lecture_file,page_number,course)` output, collect supporting IDs internally. Final freshness function remains unchanged and dependency-only.
- [x] **Step 4: Run GREEN.** `pytest tests/test_quality_gate.py tests/test_presentation_refinement.py tests/test_gate_commands.py tests/test_concept_quality.py -q -p no:cacheprovider` passes. Stale source hash and unsupported policy still return CLI 1; missing required CLI arguments remain 2.
- [x] **Step 5: Record checkpoint.** Log policy invalidation, ID agreement and phase-order evidence; conditional commit `refactor: gate publication with shared source occurrences` under same fallback.

### Task 5: Reproduction Guidance and Final Native Review

**Files:** Update README, `docs/architecture.md`, `docs/knowledge_schema.md`, `evaluation/README.md`, `scripts/README.md`, `tests/README.md`; extend cross-consumer synthetic tests in existing files. No `.gitignore` change or generated output required.

**Interfaces:** Consume complete Tasks 1-4; no additional public runtime interface.

- [x] **Step 1: Write failing cross-consumer regression.** `test_source_trace_survives_audit_repair_and_gate`: temp corpus with repeated valid evidence, structured support and second unrelated lecture. Check every consumed occurrence ID against independently indexed source/locator and compare shared lecture hashes/pages across mention/audit/gate; audit-only no writes; valid apply archives old draft and invalidates old report; explicit reevaluation produces current policy report; gated refinement succeeds and second run no-ops. Ensure unrelated source never enters repaired provenance. Test directly public Python/CLI adapters, not private internals.
- [x] **Step 2: Run RED then GREEN.** `pytest tests/test_gate_commands.py -q -p no:cacheprovider`; fix only concrete missing integration from approved scope. Verify failure first if new behavior missing; otherwise record contract already met without artificial breakage.
- [x] **Step 3: Update guidance.** Document source kinds, stable byte/locator IDs, exact vs cleaned text, complete coverage vs display cap, explicit repair hashes, structured blocked reasons/exit codes, no new persistent state, legacy/no-op compatibility and policy-1 reevaluation requirement. Update architecture before/after module seam; preserve truthful source-presence vs factual-certification distinction and single-writer/per-file publication limits.
- [x] **Step 4: Run verification and one fresh-context review.** `pytest -q -p no:cacheprovider`, `python3 -m compileall -q src/knowledge_review_agent scripts evaluation`, `git diff --check`. Inspect Git status and diff to ensure only planned files plus prior work/image. Native workflow's fresh reviewer reads spec, plan, changed files including untracked module/tests, and ledger. Review source lineage loss, mutation, scoped repair, compatibility and phase order. Do not re-review unrelated persistence internals or run production commands.
- [x] **Step 5: Resolve and deliver.** Reproduce Important/Critical findings with failing public-contract tests, fix in one regression pass, rerun full checks. Record findings, rulings, deferred minors and scope limits in ledger. Mark spec implemented and plan steps complete only after verification. Keep approved uncommitted checkout and report actual test count, checks, gate policy change and any residual limits. Conditional commit `docs: document shared source occurrence tracking` only under existing Git fallback rules.

## Self-Review and Execution Handoff

- Spec acceptance maps to Tasks 1 (identity/validation), 2 (selection/persistence), 3 (coverage/repair), 4 (gate/freshness) and 5 (cross-consumer integration/docs/review).
- Scope-bearing names/signatures above are canonical. Task 2 defines `SourceValidationError` in shared module for Task 3; no cyclic module imports. New model fields are trailing/defaulted, with no canonical metadata migration.
- Cross-consumer identity agreement means same bytes and locator yield same ID; consumers may select different source kinds. No assertion equates raw text occurrence IDs with structured occurrence IDs.
- Reviews/dispositions remain source-bound and must be renewed after gate policy change; no hidden schema conversion.
- Absent processed root stays compatible with existing duplicate-only consolidation; explicit missing contributor always blocks repair/gate. Recovery remains ahead of active record discovery, but source preflight occurs before writes.
- Native execution preference preserved from earlier approval. Plan approved by user and implemented on 2026-10-20. No production pipeline commands executed; approved uncommitted checkout retained.


## Final implementation and review evidence

Completed all five tasks on 2026-10-20. Baseline 117 tests; final suite 178 passed.
Compileall and diff checks pass. One fresh-context review found two Important
issues and one Minor; no Critical. Identityless source entries now block source
preflight. Consolidation restores original numeric page/item array order before
selection, while shared index keeps deterministic locator ordering. Five failing
regressions verified both fixes in one pass.

Deferred minor: compatibility artifacts decode already indexed JSON again.
Source files are read once, but wrapper still adds CPU/allocation for second JSON
decode. No correctness failure or measured scale impact found.

Rulings: preserve current uncommitted checkout (working-tree rather than isolated
commit review); correct synthetic partial-page fixture count (assertions retained);
retain synthetic-only production/PDF/scale boundary (production compatibility not
verified); limit review to source seam rather than baseline persistence/full
synthesis (no full factual certificate); retain per-lecture structured support
with real bounded raw-text locations for repair (no stronger exact-page semantic
classification claim); parent ran full suite while independent reviewer ran
focused probes (full-suite evidence is implementer-owned).

No production inputs, generated concept/graph pages, website or unrelated image
changed. Existing source-read, archive/no-op, repair scope, gate policy-2 and
post-format dependency-only freshness regressions pass.
