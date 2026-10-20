# Graph Presentation Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Native execution preference retained: parent implements; one fresh-context final reviewer checks complete change.

**Goal:** Export complete validated graph presentation data from matching refined records, then consume it through one checked browser contract without internal-state fallback.

**Architecture:** Deepen existing `graph_bundle.py` with explicit paths, payload validation, refined snapshots and safe publication. A pure JavaScript module validates/loads the same versioned payload; browser UI keeps presentation behavior. Internal topology generation remains separate and unchanged.

**Tech Stack:** Existing Python/pytest, standard-library JSON/path/URL/dataclass/tempfile tooling, browser ES modules, Node built-in test runner. No new npm/Python runtime dependency, schema generator or durable state.

**Spec:** [Approved graph presentation spec](../specs/2026-10-20-graph-presentation-contract-design.md), approved by user on 2026-10-20.

## Global Constraints

- Preserve prior persistence, evaluation/refinement and source occurrence work on current `superpowers-dev` checkout.
- No production ingestion, evaluation, refinement or graph regeneration during this improvement.
- Do not modify existing concept pages, graph bundles, state/deltas, raw PDFs or unrelated image.
- Current shipped site must keep working without `data/`, draft concepts or a build step.
- New exports use `schema_version: 2`; complete schema-1 presentation bundles remain readable through explicit legacy adapter.
- Relations remain exactly `prerequisite` and `related`, matching current builder.
- No layout/style redesign, relationship inference change or automatic enrichment.
- No runtime schema-fetch dependency or generic validation engine.
- No readiness evaluation or source occurrence parsing during presentation export.
- Exporter never writes internal graph state/deltas. Internal builder retains its own incremental policy; a presentation no-op does not imply a topology-state no-op.
- Single-writer assumptions remain. No claim of crash-atomic whole-site deployment.
- Use temporary synthetic fixtures/static submissions; existing packaged graph may receive read-only compatibility checks only.
- Keep approved uncommitted-checkout fallback: no staging/push/merge/new worktree, no movement or deletion of prior work/image. Native review must include untracked files, not commit range alone.

## Review Focus

1. A well-formed edge with absent source, endpoint-key disagreement or ID colliding with node must fail before Cytoscape/publication, even when statistics look plausible (Tasks 1/3).
2. URL percent encoding, literal #/&/?/%, Unicode, encoded traversal, prefix lookalikes, cross-origin targets and custom website/output roots must preserve exact refined-file identity (Tasks 1/2/3/5).
3. A final missing/outdated refined record, symlink escape or malformed metadata must preserve old graph.json and produce actionable error; stale drafts must never supply hidden enrichment (Tasks 2/4).
4. Schema-1 compatibility must preserve existing package without fetching drafts/internal graph files or repairing missing data, while unsupported/raw shapes fail clearly (Tasks 1/3/5).
5. Identical presentation must preserve bytes/mtime/timestamp despite newer caller timestamp; statistics rounding, empty/isolated graphs and source-list ordering must agree across languages (Tasks 1/2/3).

## File Map

| File | Responsibility |
| --- | --- |
| `src/knowledge_review_agent/graph_bundle.py` | Existing bundle models plus contract/path validation, legacy adapter, refined snapshots, enrichment and atomic no-op-aware export. Keep cohesive ownership. |
| `website/graph-contract.mjs` (new) | Pure payload validator, explicit legacy adapter, published-path resolver and single-bundle loader. No DOM/Cytoscape/generation logic. |
| `website/app.js`, `website/concept.js` | Thin loader/path adapters; preserve search/filter/layout/viewer behavior, remove second producer and unsafe URL defaults. |
| `website/index.html`, `website/concept.html` | Contract-aware script versions and optional declarative deployment-root attributes; no UI redesign. |
| `scripts/build_graph.py`, `evaluation/evaluate_graph.py` | Explicit path configuration, structured export failure and opt-in presentation check; preserve internal metrics API. |
| `tests/fixtures/graph_presentation/` (new) | Shared complete v1/v2/empty fixtures and cross-language invalid-case vectors. |
| `tests/graph_fixtures.py` (new) | Synthetic matched topology/refined/site trees and payload mutation helper. |
| `tests/test_graph_bundle.py`, `tests/test_graph_presentation.py` (new), `tests/test_graph_commands.py` (new) | Python contracts, snapshot/URL/publication and CLI regressions. |
| `tests/js/graph-contract.test.mjs` (new) | Node contract parity, path safety, fetch failure/no fallback and actual HTTP URL round trips. |
| `docs/graph_presentation_contract.md` (new), README/architecture/submission/evaluation/scripts/tests/website docs | Normative field rules, upgrade/reproduction and truthful boundaries. |

## Shared Interfaces and Decisions

Keep existing `GraphBundleNode`/`GraphBundleEdge` field names. `GraphBundle.schema_version` defaults to 2. Add following public contracts to `graph_bundle.py`:

```python
@dataclass(frozen=True)
class GraphPresentationPaths:
    repo_root: Path
    concepts_root: Path
    refined_root: Path
    website_root: Path

@dataclass(frozen=True)
class GraphContractIssue:
    code: str
    location: str
    message: str

class GraphContractError(ValueError):
    issues: tuple[GraphContractIssue, ...]

def validate_graph_paths(paths: GraphPresentationPaths, *,
                         graphs_root: Path | None = None) -> None: ...
def validate_graph_payload(payload: object, *, paths: GraphPresentationPaths,
                           check_files: bool = False) -> dict: ...
def load_graph_bundle(path: Path, *, paths: GraphPresentationPaths,
                      check_files: bool = False) -> dict: ...
def build_graph_bundle(nodes: list[GraphNode], edges: list[GraphEdge],
                       graphs_root: Path, generated_at: str, *,
                       paths: GraphPresentationPaths | None = None) -> GraphBundle: ...
def write_graph_bundle(graphs_root: Path, nodes: list[GraphNode], edges: list[GraphEdge],
                       generated_at: str, *,
                       paths: GraphPresentationPaths | None = None) -> Path: ...
```

`GraphContractError(issues)` stores issues and readable message; CLI serializes issues with dataclasses.asdict. Error codes: `schema_version`, `field_type`, `timestamp`, `duplicate_id`, `duplicate_key`, `dangling_endpoint`, `endpoint_key`, `unresolved_edge`, `self_edge`, `relation_type`, `stats`, `node_degree`, `published_path`, `refined_record`, `node_metadata_mismatch`, `unsafe_output`, `io_error`. Return normalized COPY from validator, never mutate caller payload. Legacy adapter is explicit private branch/helper inside validator, not a second producer.

**Root defaults:** If exporter `paths=None`, derive repo from installed checkout's module location, then conventional `knowledge_base/concepts`, `knowledge_base/refined`, `website`. Never infer repo from graphs_root. Explicit roots must be within repo; draft/refined roots must be separate/non-overlapping. Website may contain refined content in custom layouts; graph output may be outside repo when explicitly supplied. With graphs_root supplied, validate_graph_paths rejects output overlap (either direction) with concepts/refined roots and symlink output root/file before builder writes; it does not require missing draft roots to exist. Metadata path may be absolute under configured concepts/refined root or raw repo-relative path; relative paths resolve against repo, never cwd. Reject traversal and symlinks within declared input/output roots (system aliases above declared roots are permitted).

**Payload fields:** Every field currently declared in GraphBundleNode/GraphBundleEdge remains required. Optional content means empty string/list/map, not omitted field or null. Node identity/name/paths/URLs and endpoint identity strings must be nonblank; list members and hash-map keys/values are strings. Numeric ranks are real integers 1..5 (bool excluded); counts real nonnegative integers; target_resolved must be true. Keys are opaque canonical identifiers supplied by generation; browser does not port domain naming rules or rename/singularize keys. Uniqueness and endpoint matching use exact keys. Preserve educational strings exactly. Set-like lists may dedupe/sort in new exports, not in validation. Multi-course stats count distinct course identifiers, not duplicate list entries. Domain order is Unicode-code-point order, not locale-dependent sorting. Preserve unknown extension fields only when JSON-compatible/finite; never infer required values from them.

**Timestamp/rounding:** Require calendar-valid timezone-bearing ISO-8601 date-time with seconds, optional 1..6 fractional digits and Z or numeric offset; validate calendar bounds in both languages (Date.parse alone is insufficient). Half-up average degree uses exact nonnegative rational arithmetic: `floor((400*edge_count + node_count)/(2*node_count))/100` for nonempty graph, otherwise 0. Include nine edges among 400 nodes as tie case: average 0.045 must validate as 0.05, not 0.04.

**URL identity:** metadata_path is raw repo-relative refined path in v2. metadata_url is URL-encoded path relative to website directory, with no query/fragment. concept_url is configured viewer path plus exactly one `path` query whose decoded value is URL-encoded relative Markdown URL; legacy `view` query allowed only in v1. Metadata and concept URLs must target same relative directory under configured refined root and correct filenames. Reject scheme/network/absolute filesystem URLs, backslashes/control characters, malformed percent encoding, encoded traversal/separators escaping roots, prefix lookalikes and foreign-origin targets. Decode only URL layer being resolved: literal `%2F` filename requires `%252F` in resource URL and must not be recursively decoded as separator. Raw unencoded URL delimiters that change target identity fail, never guessed.

**JavaScript API:** `website/graph-contract.mjs` exports `GraphContractError extends Error` with `.issues` array using same codes/locations, `validateGraphPayload(payload, options) -> normalizedCopy`, `loadGraphData(options, fetcher = globalThis.fetch) -> Promise<normalizedBundle>` and `resolveConceptPath(rawPath, options) -> URL`. Options = `{baseUrl, repoRootUrl?, refinedRootUrl?, viewerUrl?, graphUrl?}`; URL overrides resolve relative to baseUrl and must remain same-origin. Defaults from website page URL: repo `../`, refined `../knowledge_base/refined/`, viewer `./concept.html`, graph `../knowledge_base/graphs/graph.json`. Module never reads window/document implicitly. Schema-1 normalization changes legacy metadata_path to published path derived from validated metadata_url, without changing graph/summary/stat content.

---

### Task 1: Python Presentation Contract and Shared Fixtures

**Files:** Modify `graph_bundle.py`; create `docs/graph_presentation_contract.md`, `tests/graph_fixtures.py`, `tests/test_graph_presentation.py`, `tests/fixtures/graph_presentation/valid-v2.json`, `valid-v1.json`, `empty-v2.json`, `cases.json`.

**Interfaces:** Produce GraphPresentationPaths/GraphContractIssue/GraphContractError, validate_graph_paths, validate_graph_payload and load_graph_bundle above. Fixtures expose `presentation_tree(tmp_path: Path) -> tuple[GraphPresentationPaths, list[GraphNode], list[GraphEdge]]` with two matched refined concepts and one prerequisite; expose `apply_case(payload: dict, operations: list[dict]) -> dict`. `cases.json` entries have `name`, `base` fixture filename, `operations` (`op`: `set`/`remove`, `path`: array of keys/indices, `value` for set), `valid` boolean and expected `code` for invalid cases. Test-only helpers apply operations, not production code.

- [x] **Step 1: Write failing contract tests.** `test_contract_fixture_cases` validates complete v2/v1/empty and parameterizes shared invalid vectors for wrong/missing/null field, unsupported/bool schema, invalid timestamp/calendar, rank coercion/non-finite values, duplicate/cross-kind ID, duplicate key, missing source/target, key mismatch, unresolved flag, self edge, unsupported relation, wrong degree/stats and unsafe URLs. Assert exact expected issue code/location and input unchanged. V1 normalization retains every educational/provenance field and changes legacy path only. `test_stats_rounding_and_unicode_domains` pins half-up tie and code-point ordering; isolated nodes valid. `test_bundle_loader_rejects_bad_json` checks missing/invalid JSON produces structured GraphContractError.

  Minimal assertions against two-node fixture:
  ```python
  result = validate_graph_payload(payload, paths=paths)
  assert result['schema_version'] == 2
  assert result['stats']['average_node_degree'] == 1
  assert result['nodes'][0]['degree'] == 1
  broken = apply_case(payload, [{'op': 'set', 'path': ['edges', 0, 'source'], 'value': 'absent'}])
  with pytest.raises(GraphContractError) as caught:
      validate_graph_payload(broken, paths=paths)
  assert caught.value.issues[0].code == 'dangling_endpoint'
  ```
- [x] **Step 2: Run RED.** `pytest tests/test_graph_presentation.py -q -p no:cacheprovider` fails for missing contract interfaces; inspect actual failure rather than assuming fixture validity.
- [x] **Step 3: Implement contract.** Define complete v2 field/type/graph/stat/URL validation using existing dataclass field names and repo-local rules; preserve fixture prose. Add explicit checked v1 adapter and JSON loader. `check_files=False` performs structural/path validation without metadata/Markdown reads; true additionally requires regular existing targets within refined root and existing concept viewer, rejecting symlinks. Synthetic presentation_tree creates that viewer file. Root/path preflight uses validate_graph_paths; missing draft directory is allowed for static-only consumption. No enrichment or state writes in validator. Write normative field/URL/timestamp/error rules alongside fixtures; unknown versions never repaired.
- [x] **Step 4: Run GREEN.** Same pytest command passes. Compile new Python interfaces; fixtures JSON-load successfully with standard library.
- [x] **Step 5: Record checkpoint.** Ledger RED/GREEN and contract rules; conditional commit `feat: define graph presentation contract` only if Git permissions change, otherwise approved uncommitted fallback.

### Task 2: Refined Snapshot Export and Atomic No-op Publication

**Files:** Modify `graph_bundle.py`, `tests/test_graph_bundle.py`; extend `tests/graph_fixtures.py` and `tests/test_graph_presentation.py`.

**Interfaces:** Consume Task 1 paths/validator/errors. Produce updated build_graph_bundle/write_graph_bundle signatures above; retain return types and caller-supplied timestamp. Inputs remain GraphNode/GraphEdge topology objects.

- [x] **Step 1: Write failing exporter tests.** `test_export_uses_refined_snapshot_only` supplies different draft/refined content; assert all summaries/definition/search fields derive from refined bytes, draft file reads fail if attempted, and each refined file is read once. Missing/refined-identity/version/classification/rank/course/lecture mismatch raises before writing. `test_shared_markdown_sections_preserve_content` includes fenced fake headings and repeated real sections; preserve exact selected section bodies and metadata strings, no generated prose. `test_custom_roots_and_url_roundtrip` uses nested filename `A # & ? % μ/metadata.json examples`, custom website/refined/output locations; resolve metadata_url and viewer path through same URL rules as browser and read exact original files. Test declared input root escape/symlinks and output-root/file symlinks.
  `test_invalid_last_node_preserves_existing_bundle` asserts old graph bytes/mtime retained, absent output remains absent. `test_export_noop_and_atomic_update` asserts permutation of input order/set-like lists and newer timestamp produces identical bytes/mtime/original timestamp; meaningful change replaces complete validated JSON. Simulated os.replace failure preserves old bundle and cleans temp file. Fix old unit fixture's dangling calculus endpoint by adding real matching calculus/refined record, not weakening endpoint assertions.
- [x] **Step 2: Run RED.** `pytest tests/test_graph_bundle.py tests/test_graph_presentation.py -q -p no:cacheprovider` exposes draft reads, unsafe links, blind publication or timestamp rewrites.
- [x] **Step 3: Deepen exporter.** Resolve actual relative concept directories using configured roots; capture exact refined JSON/Markdown bytes once before enrichment. Strictly validate parsed shapes/finite fields before applying existing ConceptMetadata defaults, without reopening metadata via disk loader. Check canonical key (metadata explicit key else existing normalization fallback), name, version, timestamp and graph-defining attributes against topology node; compare contribution sets independent of ordering. Use shared concept_document parser, preserve duplicate selected section content and fences. Build encoded URLs from Path operations; no substring replacements or draft fallback. Deterministically assemble v2 dataclasses/stats, validate complete payload/check files, then compare semantic payload excluding generated_at with existing valid bundle. Keep old bytes on no-op; otherwise fsync sibling temp and os.replace. Invalid old JSON may be atomically replaced by valid new export; existing read errors/symlink output reject. Exporter touches graph.json only, never internal state/deltas.
- [x] **Step 4: Run GREEN.** `pytest tests/test_graph_bundle.py tests/test_graph_presentation.py tests/test_graph_builder.py -q -p no:cacheprovider` passes with previous incremental topology assertions unchanged.
- [x] **Step 5: Record checkpoint.** Log refined-only reads, invalid-last-record protection and no-op evidence; conditional commit `refactor: publish graph bundles from refined snapshots` under same fallback.

### Task 3: Browser Contract, Single-Bundle Loader and Viewer Guard

**Files:** Create `website/graph-contract.mjs`, `tests/js/graph-contract.test.mjs`; modify `website/app.js`, `website/concept.js`, index/concept HTML script versions/root attributes.

**Interfaces:** Consume shared fixtures/normative rules from Task 1 and exported URL semantics from Task 2; produce JavaScript API defined above. Do not add browser topology/stats generation or domain canonical-name normalization.

- [x] **Step 1: Write failing Node tests.** `contract fixture parity` runs same fixtures/cases as Python and checks expected code/input immutability/v1 normalization. `calendar, half-up, unicode and empty` exercises tie case, invalid calendar dates, isolated nodes and domains. `loader fetches exactly graph bundle` supplies explicit fake fetcher recording URLs and returns real fixture bytes; assert one graph request and zero metadata/internal-node/edge requests. Missing/HTTP error/malformed JSON/unsupported graph reject with useful errors; no fallback. `published path safety and literal filename roundtrip` checks custom root options, spaces/#/&/?/%/Unicode, malformed escaping, encoded traversal/separators, external/network/absolute URLs, root-prefix lookalikes, duplicate viewer path query and wrong target filename. Start Node loopback temporary server over synthetic files and follow final URLs to assert exact metadata/Markdown content, including literal `%2F` filename. Verify concept resolver rejects invalid rawPath before fetch is attempted.
- [x] **Step 2: Run RED.** `node --test tests/js/graph-contract.test.mjs` fails for missing module/API and actual missing URL checks.
- [x] **Step 3: Implement/integrate browser adapter.** Pure module validates supported payloads and returns copy, loading only graph.json. app.js imports loader, validates before setting state/renderFilters/createCy; remove buildFallbackGraph/siteUrlFromMetadataPath/conceptViewerUrl and required-field coercions that hide contract errors. Preserve presentation fallbacks for legitimate empty optional strings. concept.js imports resolver and guards path before setting raw link/fetching Markdown; existing visible error handling catches rejected paths. HTML optional data attributes `data-graph-url`, `data-refined-root-url`, `data-repo-root-url` on document root configure custom deployment; both adapters pass corresponding options, defaults unchanged. No runtime config/schema fetch. Bump static script version strings consistently; graph fetch uses configured URL without arbitrary timestamp cache bust. Keep CSS, layout, controls, MathJax/Cytoscape runtime dependencies and content rendering unchanged.
- [x] **Step 4: Run GREEN.** Node command passes. Run Python contract/export tests again to catch cross-language fixture drift; no npm install/build step.
- [x] **Step 5: Record checkpoint.** Log fixture parity, request inventory and special-character HTTP round trips; conditional commit `fix: validate graph bundles before browser presentation` under same fallback.

### Task 4: Explicit CLI Export and Presentation Checks

**Files:** Modify `scripts/build_graph.py`, `evaluation/evaluate_graph.py`; create `tests/test_graph_commands.py`. Existing `graph_evaluation.evaluate_graph` and internal metrics result stay unchanged.

**Interfaces:** Build CLI adds `--repo-root`, `--refined`, `--site` alongside existing `--concepts`/`--graphs`; unset concepts/refined/site/graphs paths resolve conventionally under explicit/default repo root; --repo-root must not leave default graph output pointing at another checkout. Construct GraphPresentationPaths explicitly and call validate_graph_paths(paths, graphs_root=graphs_root); preflight root/output topology before graph builder can write into invalid location. Evaluation CLI adds `--presentation` plus same root options; default mode still prints existing internal heuristic metrics. Presentation mode calls load_graph_bundle(graphs_root/'graph.json', paths=..., check_files=True), requiring published files only, not draft root existence or raw/internal graph data.

- [x] **Step 1: Write failing subprocess tests.** `test_build_cli_exports_v2_and_noops` runs only synthetic matched corpus; first build succeeds, second preserves graph.json bytes/mtime and unchanged graph state/delta inventory. Custom output directory does not alter URLs. `test_export_failure_preserves_presentation` changes draft node version while refined stays old; assert CLI exit 1 with structured error/issues and old graph unchanged; internal graph state may advance per documented separation. Bad output overlap/symlink rejected before graph builder writes. `test_presentation_check_requires_only_static_package` removes drafts/internal files/data from temp package, checks valid v1/v2 exit 0 and structured counts; malformed/missing bundle, unsafe/missing refined link or unsupported schema exit 1 without file changes. Default internal metric CLI output keys remain compatible; invalid arguments remain argparse 2.
- [x] **Step 2: Run RED.** `pytest tests/test_graph_commands.py -q -p no:cacheprovider` exposes missing flags, old writer behavior or missing structured errors.
- [x] **Step 3: Wire CLI modes.** Call existing graph builder for internal state then validated exporter with explicit paths. Catch GraphContractError plus normal read/JSON/value failures, print stderr JSON `error`/`issues`, return 1. Presentation check prints stdout `{valid: true, schema_version, node_count, edge_count}` on success; do not present internal heuristic integrity score as contract certificate. Root validation permits missing drafts for presentation-only check and rejects unsafe overlapping output for build before mutation. Do not invoke readiness evaluation, source parsing or refinement.
- [x] **Step 4: Run GREEN.** `pytest tests/test_graph_commands.py tests/test_graph_builder.py tests/test_graph_presentation.py tests/test_graph_bundle.py -q -p no:cacheprovider` passes; Node contract tests remain green.
- [x] **Step 5: Record checkpoint.** Log CLI statuses/static-only dependency test and topology-vs-publication distinction; conditional commit `feat: add explicit graph presentation checks` under same fallback.

### Task 5: Static Submission Acceptance, Guidance and Final Native Review

**Files:** Extend Python/Node integration tests as needed; update README, website/README, docs/architecture, docs/submission_manifest, evaluation/README, scripts/README, tests/README and normative contract doc. No tracked generated files or ignore/deletion changes.

**Interfaces:** Consume Tasks 1-4; no new runtime interface. Reproduction commands are `pytest -q -p no:cacheprovider`, `node --test tests/js/graph-contract.test.mjs`, `python3 -m compileall -q src/knowledge_review_agent scripts evaluation`, `git diff --check`.

- [x] **Step 1: Add final public-path acceptance.** `test_python_export_consumed_by_browser_contract` generates v2 over synthetic matched records then passes real exported JSON to Node module and follows actual metadata/viewer URLs over loopback server. No independent expected payload constructed from exporter internals. Assert two nodes/one edge and original special-character Markdown content; missing draft/data/nodes/edges/state does not matter. Read-only compatibility test loads existing shipped v1 file through Python and JavaScript validators, checks files without rewriting anything; report current observed count rather than hardcode production dataset count in permanent tests.
- [x] **Step 2: Run integration checks and browser smoke.** New tests must show intended failure first when preceding implementation missing; if already covered/GREEN, record fact without artificial breakage. Serve temporary minimal package containing website + synthetic refined records + graph.json ONLY. Use available browser tooling to load graph, search/select synthetic concept, open viewer and verify exact text and URL. Repeat using fixture v1, then broken endpoint fixture: useful error and no graph initialization. Inspect requests for absence of draft/data/raw-node/edge fetches. Browser smoke may use existing external Cytoscape/MathJax runtimes; report external load failure explicitly instead of claiming rendering verified. Always stop own temporary server and retain results in ignored plan workspace; do not operate production site/server.
- [x] **Step 3: Update reproduction/contract docs.** State v2 export/v1 adapter, field/error rules and published-root/URL encoding behavior. Show explicit build flags and presentation-check mode, explain reevaluate/refine before rebuilding topology when refined content stale. Distinguish structural contract from factual/readiness gate or heuristic score. Describe atomic single-file/no-op behavior and internal-state independence. Submission manifest must identify graph.json as only runtime graph payload; previously tracked nodes.json/edges.json may remain shipped diagnostics, not required browser inputs. Do not delete/untrack them. Preserve current optional external runtime/network limitations.
- [x] **Step 4: Verify and request one fresh-context review.** Run complete Python/Node/compile/diff checks, inspect status and graph/concept/website-content inventories against baseline. Ensure only planned source/website code/docs/tests plus prior work/image changed, no generated production bundle. Reviewer reads approved spec/plan/Review Focus, ledger rulings and current working tree including untracked JS/tests. Review source/refined mismatch, path encoding/escape, bad endpoints/stats, v1 preservation, publication no-ops and no hidden browser producer. No reviewer subagents or production builds.
- [x] **Step 5: Fix and deliver.** Reproduce Important/Critical findings with failing tests, fix in one regression pass, rerun full checks. Record rulings/deferred minors/declined scope; preserve user-approved uncommitted workspace. Mark completion only with actual verification output. Report actual Python/Node counts, browser smoke result, compatibility and any residual limitations. Conditional commit `docs: document graph presentation contract` under same sandbox fallback, no integration prompt beyond existing keep-as-is choice.

## Self-Review and Handoff

- Task 1 defines shared shape/path/error interfaces; Task 2 consumes them for export; Task 3 consumes same fixture contract in browser; Task 4 consumes public Python APIs; Task 5 exercises complete producer/consumer seam.
- Version 2 changes guarantees/path authority, not field names. Legacy adapter uses validated published URLs; it does not convert missing raw edge shapes or fabricate graph details. Required content fields may be empty, never silently omitted.
- Input arrays are sorted only by producer where set-like; educational strings and shared fixtures are not rewritten by validators. Explicit URL decoding layers and code-point/rounding/calendar rules prevent cross-language guesswork.
- Exporter defaults depend on checkout location, not output directory. Browser defaults preserve conventional package; explicit root overrides are wired through both HTML adapters for custom layouts.
- Root/output preflight precedes build writes; later refined mismatch may still follow internal topology update. This is documented separation, not a whole-graph transaction promise.
- No existing production bundle migrated; current v1 compatibility checked read-only. Old dangling-endpoint unit fixture becomes valid complete graph instead of weakening validation.
- Plan self-reviewed for coverage/signatures/scope and executable verification commands. Native preference retained; approved plan implemented and verified on 2026-10-20.

## Completion evidence

Implemented on 2026-10-20. Final checks: 237 Python tests, 33 Node tests,
compileall and git diff --check pass. Browser smoke on synthetic static-only
package verifies v1/v2 graph rendering, search/selection/refined viewer, malformed
endpoint error and draft-path rejection without internal-file fetches. Existing
167 graph/refined files unchanged by SHA-256.

Fresh review found output ancestor symlink bypass and publication permissions
regression (regraded Important); both reproduced RED and fixed GREEN in one pass.
New files use 0644; replacements preserve existing mode. Rare Unicode domain
whitespace mismatch between Python strip and JavaScript trim remains deferred.
Review scope/rulings recorded in retained plan workspace; production regeneration,
factual quality, broad Markdown security, concurrent whole-site writes and CDN
reliability remain outside this change's guarantees. Approved uncommitted checkout
retained; no staging, commit, push, merge or production pipeline run.
