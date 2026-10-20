"""Source-bound eligibility evidence shared by evaluation and refinement."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timedelta
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import unquote, urlsplit

from .concept_document import canonical_section_name, local_document_links, parse_concept_document
from .concept_store import concept_history_root, load_concept_metadata
from .evaluation import evaluate_definition_quality, evaluate_consolidation
from .source_occurrences import index_sources
from .utils import normalize_concept_key, normalize_spaces

GATE_SCHEMA_VERSION = 1
GATE_POLICY_VERSION = "3"


class GateError(RuntimeError):
    pass


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode()


def content_digest(value: object) -> str:
    return sha256(canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class GatePaths:
    concepts_root: Path
    processed_root: Path
    reviews_root: Path
    asset_roots: tuple[Path, ...] = ()


@dataclass(frozen=True)
class GateFinding:
    code: str
    concept_key: str
    path: str
    severity: str
    details: dict
    remediation: str
    finding_id: str
    resolved_by: tuple[str, ...] = ()


@dataclass(frozen=True)
class GateConcept:
    relative_dir: str
    concept_key: str
    markdown: bytes
    metadata: bytes
    fingerprint: str
    supported_pages: tuple[dict, ...] = ()
    source_occurrence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class GateSnapshot:
    paths: GatePaths
    manifest: dict[str, str]
    fingerprint: str
    concepts: tuple[GateConcept, ...]
    findings: tuple[GateFinding, ...]
    files: dict[str, bytes] = field(default_factory=dict, repr=False)


def paths_payload(paths: GatePaths) -> dict:
    return {"concepts": str(paths.concepts_root.resolve()), "processed": str(paths.processed_root.resolve()),
            "reviews": str(paths.reviews_root.resolve()), "assets": [str(p.resolve()) for p in paths.asset_roots]}


def _safe_relative(path: str) -> Path:
    relative = Path(path)
    if not path or relative.is_absolute() or any(p in {"", ".", ".."} for p in path.split("/")):
        raise GateError(f"Unsafe relative input path: {path}")
    return relative


def _checked_path(path: Path, root: Path) -> Path:
    # Permit system aliases in root parents, reject symlinks within declared root.
    if root.is_symlink():
        raise GateError(f"Symlink input root: {root}")
    relative = path.absolute().relative_to(root.absolute())
    cursor = root
    for part in relative.parts:
        cursor /= part
        if cursor.is_symlink():
            raise GateError(f"Symlink input path: {cursor}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise GateError(f"Input outside configured root: {path}")
    return path


def _finding(code, key, path, details, severity="hard") -> GateFinding:
    identity = {"code": code, "concept_key": key, "path": path, "details": details}
    remediation = ("Resolve this finding with a current evidence-backed reviewer decision."
                   if severity == "review" else "Fix draft/source inputs, then evaluate again; refinement remains blocked.")
    return GateFinding(code, key, path, severity, details, remediation, content_digest(identity))


def capture_gate_snapshot(paths: GatePaths) -> GateSnapshot:
    manifest: dict[str, str] = {}
    files: dict[str, bytes] = {}
    findings = []
    concepts = []
    root = paths.concepts_root
    history = concept_history_root(root)
    roots = [("concepts", root), ("history", history), ("processed", paths.processed_root)]
    roots += [(f"assets/{i}", p) for i, p in enumerate(paths.asset_roots)]

    def issue(code, key, path, detail, severity="hard"):
        finding = _finding(code, key, str(path), detail, severity)
        if not any(f.finding_id == finding.finding_id for f in findings):
            findings.append(finding)

    def read(path: Path, allowed: Path, label: str, dependencies=None) -> bytes:
        _checked_path(path, allowed)
        name = f"{label}/{path.absolute().relative_to(allowed.absolute()).as_posix()}"
        if name not in files:
            if not path.is_file():
                manifest[name] = sha256(b"missing input").hexdigest()
                raise GateError(f"Missing regular input file: {path}")
            files[name] = path.read_bytes()
            manifest[name] = sha256(files[name]).hexdigest()
        if dependencies is not None:
            dependencies[name] = manifest[name]
        return files[name]

    try:
        _checked_path(root, root)
        if not root.is_dir():
            raise GateError(f"Missing concepts root: {root}")
        all_paths = sorted(root.rglob("*"))
        for path in all_paths:
            if path.is_symlink():
                issue("unsafe_input", "", path.relative_to(root), {"error": "Symlink in concepts tree"})
        directories = sorted({p.parent for p in all_paths if p.name in {"metadata.json", "concept.md"}})
    except (OSError, ValueError, GateError) as exc:
        directories = []
        issue("invalid_corpus", "", root, {"error": str(exc)})
    if not directories:
        issue("empty_corpus", "", root, {"error": "No concept records"})
    # Capture referenced bytes once before interpreting source support. The same
    # manifest reader supplies both index construction and per-concept dependencies.
    references = set()
    for directory in directories:
        try:
            payload = json.loads(read(directory / "metadata.json", root, "concepts"))
            if isinstance(payload, dict) and isinstance(payload.get("contributing_lecture_files"), list):
                references.update(r for r in payload["contributing_lecture_files"] if isinstance(r, str))
        except (OSError, ValueError, TypeError, GateError):
            pass  # The record loop emits actionable input findings.
    source_bytes = []
    for reference in sorted(references):
        try:
            source_bytes.append((reference, read(paths.processed_root / _safe_relative(reference),
                                                paths.processed_root, "processed")))
        except (OSError, ValueError, TypeError, GateError):
            pass  # Preserve missing-input manifest entries and report against each contributor.
    source_index = index_sources(source_bytes)
    keys = {}
    for directory in directories:
        relative = directory.relative_to(root).as_posix()
        dependencies = {}
        key = ""
        try:
            if any(other != directory and other in directory.parents for other in directories):
                raise GateError("Nested concept records are ambiguous")
            markdown = read(directory / "concept.md", root, "concepts", dependencies)
            raw = read(directory / "metadata.json", root, "concepts", dependencies)
            payload = json.loads(raw)
            canonical_json(payload)  # Reject non-finite JSON values before typed loading.
            if not isinstance(payload, dict):
                raise GateError("Concept metadata must be an object")
            for name in ("concept_name", "canonical_key", "definition", "domain", "topic"):
                if not isinstance(payload.get(name), str):
                    raise GateError(f"Missing/invalid metadata string: {name}")
            for name in ("contributing_courses", "contributing_lecture_files", "aliases"):
                value = payload.get(name, [])
                if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
                    raise GateError(f"Invalid metadata list: {name}")
            hashes = payload.get("source_lecture_hashes")
            if not isinstance(hashes, dict):
                raise GateError("Missing/invalid source lecture hashes")
            key = normalize_concept_key(payload["canonical_key"])
            if not key or not payload["concept_name"].strip():
                raise GateError("Missing canonical identity")
            if key in keys:
                issue("duplicate_key", key, relative, {"other_record": keys[key]})
            keys[key] = relative
            if not payload["domain"].strip() or not payload["topic"].strip():
                issue("missing_classification", key, relative, {"error": "Domain and topic required"})
            document = parse_concept_document(markdown.decode("utf-8"))
            definitions = [normalize_spaces(s.content) for s in document.sections
                           if canonical_section_name(s.heading) == "Definition"]
            definition = normalize_spaces(payload["definition"])
            if (not document.title or not definition or not definitions or
                    normalize_concept_key(definition) in {normalize_concept_key(key), normalize_concept_key(payload["concept_name"])} or
                    re.match(r"(?i)(?:tbd|todo)\b", definition) or
                    re.fullmatch(r"(?i)(unknown|not available|needs review|definition missing)(?:[.! ]*| *:.*)", definition)):
                issue("missing_definition", key, relative, {"error": "Usable metadata and Markdown definition/title required"})
            elif any(d != definition for d in definitions):
                issue("definition_mismatch", key, relative, {"metadata": definition, "markdown": definitions})
            metadata = load_concept_metadata(directory / "metadata.json")
            if definition and evaluate_definition_quality(metadata) < .55:
                issue("weak_definition", key, relative, {"definition": definition}, "review")
            conflicts = payload.get("persistence_conflicts", [])
            if not isinstance(conflicts, list) or any(not isinstance(c, dict) for c in conflicts):
                raise GateError("Invalid persistence conflicts")
            for conflict in conflicts:
                issue("persistence_conflict", key, relative, conflict, "review")
            for section in document.sections:
                if canonical_section_name(section.heading).lower() == "quality review" and section.content.strip():
                    issue("quality_review", key, relative, {"content": section.content.strip()}, "review")
            courses = set(payload.get("contributing_courses", []))
            lectures = payload.get("contributing_lecture_files", [])
            if not courses or not lectures:
                issue("missing_provenance", key, relative, {"error": "Courses and contributing lectures required"})
            supported = []
            seen_courses = set()
            occurrence_ids = []
            for reference in lectures:
                try:
                    read(paths.processed_root / _safe_relative(reference), paths.processed_root, "processed", dependencies)
                    matches = source_index.find(key, [payload["concept_name"], *payload.get("aliases", [])],
                        lecture_hashes={reference: hashes.get(reference)}, allowed_courses=courses)
                    if matches.issues:
                        raise GateError("; ".join(i.code + ": " + i.message for i in matches.issues))
                    if not matches.occurrences:
                        raise GateError(f"No explicit concept/page support: {reference}")
                    for occurrence in matches.occurrences:
                        course = occurrence.source.course
                        supported.append({"lecture_file": reference, "page_number": occurrence.page_number, "course": course})
                        occurrence_ids.append(occurrence.occurrence_id)
                        seen_courses.add(course)
                except (OSError, ValueError, KeyError, TypeError, AttributeError, OverflowError, GateError) as exc:
                    issue("invalid_source", key, relative, {"lecture_file": reference, "error": str(exc)})
            supported = [dict(lecture_file=p, page_number=n, course=c) for p, n, c in
                         sorted({(p["lecture_file"], p["page_number"], p["course"]) for p in supported})]
            if courses - seen_courses:
                issue("unverified_course", key, relative, {"courses": sorted(courses - seen_courses)})
            for destination in local_document_links(markdown.decode("utf-8")):
                try:
                    url = urlsplit(destination)
                    asset = directory / unquote(url.path)
                    # Select by resolved location, but validate the original path for symlinks.
                    allowed = next(((label, allowed) for label, allowed in roots
                                    if asset.resolve().is_relative_to(allowed.resolve())), None)
                    if not allowed:
                        raise GateError(f"Asset outside configured roots: {destination}")
                    label, allowed_root = allowed
                    # Resolve parent traversal before lexical containment checks.
                    cursor = directory
                    for part in Path(unquote(url.path)).parts:
                        cursor = cursor.parent if part == ".." else cursor / part
                        if cursor.is_symlink():
                            raise GateError(f"Symlink evidence path: {cursor}")
                    lexical = Path(os.path.normpath(asset.absolute()))
                    read(lexical, allowed_root.absolute(), label, dependencies)
                except (OSError, ValueError, GateError) as exc:
                    issue("invalid_asset", key, relative, {"destination": destination, "error": str(exc)})
            fingerprint = content_digest({"policy": GATE_POLICY_VERSION,
                "roots": {k: v for k, v in paths_payload(paths).items() if k != "reviews"}, "inputs": dependencies})
            concepts.append(GateConcept(relative, key, markdown, raw, fingerprint,
                tuple(supported), tuple(sorted(set(occurrence_ids)))))
        except (OSError, ValueError, KeyError, TypeError, AttributeError, OverflowError, GateError) as exc:
            issue("invalid_record", key, relative, {"error": str(exc)})
    try:
        if paths.reviews_root.exists():
            for review in sorted(paths.reviews_root.rglob("*")):
                _checked_path(review, paths.reviews_root)
                if review.is_file():
                    read(review, paths.reviews_root, "reviews")
        if history.exists():
            _checked_path(history, history)
            transactions = history / "transactions"
            if transactions.exists():
                _checked_path(transactions, history)
                for transaction in sorted(transactions.iterdir()):
                    _checked_path(transaction, history)
                    journal = transaction / "journal.json"
                    if not journal.exists():
                        continue
                    raw = read(journal, history, "history")
                    body = json.loads(raw)
                    identity = sha256(json.dumps({**body, "state": "prepared"}, sort_keys=True, ensure_ascii=True).encode()).hexdigest()
                    if body.get("state") != "committed" or body.get("schema_version") != 1 or identity != transaction.name:
                        issue("pending_persistence", "", journal, {"error": "Run consolidation recovery before evaluation"})
    except (OSError, ValueError, TypeError, GateError) as exc:
        issue("pending_persistence", "", history, {"error": str(exc)})
    fingerprint = content_digest({"policy": GATE_POLICY_VERSION, "schema": GATE_SCHEMA_VERSION,
                                  "roots": paths_payload(paths), "manifest": manifest})
    return GateSnapshot(paths, dict(sorted(manifest.items())), fingerprint, tuple(concepts),
                        tuple(sorted(findings, key=lambda f: f.finding_id)), files)


def evaluate_readiness(snapshot: GateSnapshot) -> tuple[GateFinding, ...]:
    return snapshot.findings


def _hex(value) -> bool:
    return isinstance(value, str) and re.fullmatch("[0-9a-f]{64}", value) is not None


def _review_payload(raw: bytes, path: str) -> dict:
    record = json.loads(raw)
    required = {"schema_version", "reviewer", "reviewed_at", "rationale", "concept_key",
                "concept_fingerprint", "resolutions", "record_id"}
    if not isinstance(record, dict) or set(record) != required or type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise GateError("Unsupported review schema")
    if not _hex(record["record_id"]) or record["record_id"] != content_digest({k: v for k, v in record.items() if k != "record_id"}):
        raise GateError("Review content identity mismatch")
    if Path(path).name != f"{record['record_id']}.json":
        raise GateError("Review filename must match content identity")
    for name in ("reviewer", "reviewed_at", "rationale", "concept_key"):
        if not isinstance(record[name], str) or not record[name].strip():
            raise GateError(f"Missing review {name}")
    timestamp = datetime.fromisoformat(record["reviewed_at"].replace("Z", "+00:00"))
    if timestamp.utcoffset() != timedelta(0):
        raise GateError("Review timestamp must identify UTC")
    if not _hex(record["concept_fingerprint"]) or not isinstance(record["resolutions"], list) or not record["resolutions"]:
        raise GateError("Review needs fingerprint and explicit findings")
    ids = set()
    for resolution in record["resolutions"]:
        if not isinstance(resolution, dict) or set(resolution) != {"finding_id", "finding_digest", "disposition", "citations"}:
            raise GateError("Invalid review resolution")
        if not _hex(resolution["finding_id"]) or not _hex(resolution["finding_digest"]) or resolution["finding_id"] in ids:
            raise GateError("Invalid/duplicate reviewed finding")
        ids.add(resolution["finding_id"])
        if resolution["disposition"] not in {"accepted_with_evidence", "not_applicable"}:
            raise GateError("Unsupported review disposition")
        if not isinstance(resolution["citations"], list) or not resolution["citations"]:
            raise GateError("Evidence-backed citation required")
        for citation in resolution["citations"]:
            if not isinstance(citation, dict) or set(citation) != {"lecture_file", "page_number"}:
                raise GateError("Invalid review citation")
            _safe_relative(citation["lecture_file"])
            if type(citation["page_number"]) is not int or citation["page_number"] <= 0:
                raise GateError("Invalid review page number")
    return record


def _resolved_findings(snapshot: GateSnapshot) -> tuple[list[GateFinding], list[dict]]:
    findings = list(snapshot.findings)
    by_id = {f.finding_id: f for f in findings}
    concepts = {c.concept_key: c for c in snapshot.concepts}
    decisions: dict[str, list[tuple[str, str]]] = {}
    references = []
    for path, raw in sorted(snapshot.files.items()):
        if not path.startswith("reviews/"):
            continue
        try:
            record = _review_payload(raw, path)
            concept = concepts.get(record["concept_key"])
            if concept is None or concept.fingerprint != record["concept_fingerprint"]:
                continue  # Valid old decisions remain historical, never current approval.
            supported = {(p["lecture_file"], p["page_number"]) for p in concept.supported_pages}
            pending = []
            for resolution in record["resolutions"]:
                finding = by_id.get(resolution["finding_id"])
                if finding is None or finding.concept_key != concept.concept_key or finding.severity != "review":
                    raise GateError("Review cannot resolve absent, other-concept, or hard finding")
                if resolution["finding_digest"] != content_digest(finding.details):
                    raise GateError("Review finding content is stale")
                if any((c["lecture_file"], c["page_number"]) not in supported for c in resolution["citations"]):
                    raise GateError("Review cites unsupported source page")
                pending.append((finding.finding_id, resolution["disposition"]))
            for finding_id, disposition in pending:
                decisions.setdefault(finding_id, []).append((record["record_id"], disposition))
            references.append({"record_id": record["record_id"], "path": path,
                               "sha256": snapshot.manifest[path]})
        except (ValueError, TypeError, KeyError, GateError) as exc:
            findings.append(_finding("invalid_review", "", path, {"error": str(exc)}))
    result = []
    for finding in findings:
        choices = decisions.get(finding.finding_id, [])
        if len({choice[1] for choice in choices}) > 1:
            result.append(_finding("conflicting_reviews", finding.concept_key, finding.path,
                                   {"finding_id": finding.finding_id, "decisions": sorted(choices)}))
        elif choices:
            finding = replace(finding, resolved_by=tuple(sorted({choice[0] for choice in choices})))
        result.append(finding)
    return sorted(result, key=lambda f: f.finding_id), sorted(references, key=lambda r: r["path"])


def _concept_payloads(snapshot: GateSnapshot) -> list[dict]:
    return [{"relative_dir": c.relative_dir, "concept_key": c.concept_key, "fingerprint": c.fingerprint,
             "supported_pages": list(c.supported_pages)} for c in snapshot.concepts]


def _finding_payloads(findings) -> list[dict]:
    return [{**asdict(f), "resolved_by": list(f.resolved_by)} for f in findings]


def evaluate_for_refinement(paths: GatePaths) -> dict:
    snapshot = capture_gate_snapshot(paths)
    findings, references = _resolved_findings(snapshot)
    try:
        diagnostics = evaluate_consolidation(paths.concepts_root).to_dict()
        canonical_json(diagnostics)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as exc:
        diagnostics = {"unavailable": str(exc)}
    report = {"schema_version": GATE_SCHEMA_VERSION, "policy_version": GATE_POLICY_VERSION,
        "evaluator_kind": "heuristic_with_source_reference_checks", "roots": paths_payload(paths),
        "manifest": snapshot.manifest, "fingerprint": snapshot.fingerprint,
        "concepts": _concept_payloads(snapshot), "diagnostics": diagnostics,
        "findings": _finding_payloads(findings), "review_references": references,
        "eligibility": "blocked" if any(f.severity == "hard" or not f.resolved_by for f in findings) else "pass"}
    report["report_id"] = content_digest(report)
    return report


def _report_paths(report: dict) -> GatePaths:
    roots = report["roots"]
    if not isinstance(roots, dict) or set(roots) != {"concepts", "processed", "reviews", "assets"}:
        raise GateError("Invalid report roots")
    if not isinstance(roots["assets"], list):
        raise GateError("Invalid asset roots")
    for root in [roots["concepts"], roots["processed"], roots["reviews"], *roots["assets"]]:
        if not isinstance(root, str) or not Path(root).is_absolute():
            raise GateError("Report roots must be absolute paths")
    return GatePaths(Path(roots["concepts"]), Path(roots["processed"]), Path(roots["reviews"]), tuple(map(Path, roots["assets"])))


def _validate_report(report: dict) -> None:
    required = {"schema_version", "policy_version", "evaluator_kind", "roots", "manifest", "fingerprint",
                "concepts", "diagnostics", "findings", "review_references", "eligibility", "report_id"}
    if not isinstance(report, dict) or set(report) != required:
        raise GateError("Not a complete eligibility report")
    if type(report["schema_version"]) is not int or report["schema_version"] != GATE_SCHEMA_VERSION or report["policy_version"] != GATE_POLICY_VERSION:
        raise GateError("Unsupported evaluation schema/policy")
    if report["evaluator_kind"] != "heuristic_with_source_reference_checks":
        raise GateError("Unsupported evaluator kind")
    if not _hex(report["report_id"]) or report["report_id"] != content_digest({k: v for k, v in report.items() if k != "report_id"}):
        raise GateError("Evaluation report content identity mismatch")
    _report_paths(report)
    if not isinstance(report["manifest"], dict) or not _hex(report["fingerprint"]):
        raise GateError("Invalid report input manifest")
    for path, digest in report["manifest"].items():
        _safe_relative(path)
        if not _hex(digest):
            raise GateError("Invalid manifest digest")
    if not isinstance(report["concepts"], list) or not isinstance(report["findings"], list) or not isinstance(report["diagnostics"], dict) or not isinstance(report["review_references"], list):
        raise GateError("Invalid report collections")
    seen = set()
    for concept in report["concepts"]:
        if not isinstance(concept, dict) or set(concept) != {"relative_dir", "concept_key", "fingerprint", "supported_pages"}:
            raise GateError("Invalid report concept")
        _safe_relative(concept["relative_dir"])
        if not isinstance(concept["concept_key"], str) or not concept["concept_key"] or not _hex(concept["fingerprint"]) or not isinstance(concept["supported_pages"], list):
            raise GateError("Invalid report concept identity")
    blocked = not report["concepts"]
    for finding in report["findings"]:
        if not isinstance(finding, dict) or set(finding) != {"code", "concept_key", "path", "severity", "details", "remediation", "finding_id", "resolved_by"}:
            raise GateError("Invalid report finding")
        if any(not isinstance(finding[name], str) for name in ("code", "concept_key", "path", "remediation")) or not isinstance(finding["details"], dict):
            raise GateError("Invalid finding fields")
        identity = {k: finding[k] for k in ("code", "concept_key", "path", "details")}
        if finding["finding_id"] != content_digest(identity) or finding["finding_id"] in seen:
            raise GateError("Invalid/duplicate finding identity")
        seen.add(finding["finding_id"])
        if finding["severity"] not in {"hard", "review"} or not isinstance(finding["resolved_by"], list) or any(not _hex(v) for v in finding["resolved_by"]):
            raise GateError("Invalid finding resolution")
        if finding["severity"] == "hard" and finding["resolved_by"]:
            raise GateError("Hard failure cannot be reviewed away")
        blocked |= finding["severity"] == "hard" or not finding["resolved_by"]
    if report["eligibility"] != ("blocked" if blocked else "pass"):
        raise GateError("Evaluation decision contradicts findings")


def load_evaluation_report(report_path: Path) -> dict:
    try:
        if report_path.is_symlink():
            raise GateError("Symlink evaluation report")
        report = json.loads(report_path.read_bytes())
        _validate_report(report)
        if report_path.name != f"{report['report_id']}.json":
            raise GateError("Evaluation filename must match report identity")
        return report
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise GateError(f"Invalid evaluation report {report_path}: {exc}") from exc


def write_evaluation_report(report: dict, reports_root: Path) -> Path:
    _validate_report(report)
    paths = _report_paths(report)
    for root in (paths.concepts_root, paths.processed_root, paths.reviews_root, concept_history_root(paths.concepts_root), *paths.asset_roots):
        if reports_root.resolve().is_relative_to(root.resolve()):
            raise GateError("Evaluation reports must be outside input roots")
    if reports_root.is_symlink():
        raise GateError("Symlink report output root")
    path = reports_root / f"{report['report_id']}.json"
    content = canonical_json(report)
    if path.exists() or path.is_symlink():
        if path.is_symlink() or path.read_bytes() != content:
            raise GateError(f"Existing evaluation evidence differs: {path}")
        return path
    reports_root.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=reports_root, prefix=".gate-")
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return path


def require_eligible_report(report_path: Path | None, concepts_root: Path) -> GateSnapshot:
    if report_path is None:
        raise GateError("Evaluation report required before refinement")
    report = load_evaluation_report(report_path)
    paths = _report_paths(report)
    if paths.concepts_root.resolve() != concepts_root.resolve():
        raise GateError("Evaluation belongs to a different concepts root")
    if report["eligibility"] != "pass":
        raise GateError("Evaluation blocked; resolve findings and evaluate again")
    snapshot = capture_gate_snapshot(paths)
    if snapshot.fingerprint != report["fingerprint"] or snapshot.manifest != report["manifest"]:
        raise GateError("Evaluation is stale; inputs changed")
    findings, references = _resolved_findings(snapshot)
    if (_finding_payloads(findings) != report["findings"] or references != report["review_references"] or
            _concept_payloads(snapshot) != report["concepts"]):
        raise GateError("Evaluation evidence does not match current readiness")
    return snapshot


def assert_gate_snapshot_current(snapshot: GateSnapshot) -> None:
    """Verify exact dependency bytes and discovery membership, without content evaluation."""
    paths = snapshot.paths
    roots = {"concepts": paths.concepts_root, "processed": paths.processed_root,
             "reviews": paths.reviews_root, "history": concept_history_root(paths.concepts_root)}
    roots.update({f"assets/{i}": p for i, p in enumerate(paths.asset_roots)})
    try:
        identity = content_digest({"policy": GATE_POLICY_VERSION, "schema": GATE_SCHEMA_VERSION,
                                   "roots": paths_payload(paths), "manifest": snapshot.manifest})
        if identity != snapshot.fingerprint:
            raise GateError("Input roots changed")
        for name, digest in snapshot.manifest.items():
            label = next(label for label in sorted(roots, key=len, reverse=True) if name.startswith(label + "/"))
            root = roots[label]
            path = root / name[len(label) + 1:]
            _checked_path(path, root)
            if not path.is_file() or sha256(path.read_bytes()).hexdigest() != digest:
                raise GateError("Input bytes changed")
        discovered = set()
        for label in ("concepts", "reviews"):
            root = roots[label]
            _checked_path(root, root)
            for path in root.rglob("*"):
                _checked_path(path, root)
                if path.is_file() and (label == "reviews" or path.name in {"concept.md", "metadata.json"}):
                    discovered.add(f"{label}/{path.relative_to(root).as_posix()}")
        history = roots["history"]
        _checked_path(history, history)
        transactions = history / "transactions"
        _checked_path(transactions, history)
        for transaction in transactions.iterdir() if transactions.exists() else ():
            _checked_path(transaction, history)
            journal = transaction / "journal.json"
            _checked_path(journal, history)
            if journal.exists():
                discovered.add(f"history/{journal.relative_to(history).as_posix()}")
        expected = {name for name in snapshot.manifest if name.startswith("reviews/") or
                    name.startswith("history/transactions/") and name.endswith("/journal.json") or
                    name.startswith("concepts/") and Path(name).name in {"concept.md", "metadata.json"}}
        if discovered != expected:
            raise GateError("Input membership changed")
    except (OSError, ValueError, StopIteration, GateError) as exc:
        raise GateError("Evaluation became stale during preparation; no publication performed") from exc
