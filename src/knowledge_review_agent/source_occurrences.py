"""Immutable source locations shared by synthesis, audit and eligibility policy."""
from __future__ import annotations

from collections.abc import Iterable, Mapping, Set as AbstractSet
from dataclasses import dataclass, field
from hashlib import sha256
import json
import math
from pathlib import Path
import re
from types import MappingProxyType

from .utils import normalize_concept_key

SOURCE_OCCURRENCE_POLICY_VERSION = "1"


@dataclass(frozen=True)
class SourceIssue:
    lecture_file: str
    code: str
    locator: str
    message: str


class SourceValidationError(ValueError):
    def __init__(self, issues: tuple[SourceIssue, ...]):
        self.issues = issues
        super().__init__("; ".join(f"{i.lecture_file}:{i.locator}: {i.code}: {i.message}" for i in issues))


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class SourceRecord:
    relative_path: str
    sha256: str
    raw: bytes
    course_id: str
    course_name: str
    source_pdf: str
    page_count: int
    payload: Mapping[str, object]

    @property
    def course(self) -> str:
        return self.course_id or self.course_name


@dataclass(frozen=True)
class SourceOccurrence:
    occurrence_id: str
    source: SourceRecord
    page_number: int
    json_pointer: str
    kind: str
    labels: tuple[str, ...]
    canonical_key: str
    identities: tuple[str, ...]
    text: str
    page_heading: str
    line_number: int = 0
    start: int = 0
    end: int = 0
    item: Mapping[str, object] = field(default_factory=lambda: MappingProxyType({}))


@dataclass(frozen=True)
class SourceMatches:
    occurrences: tuple[SourceOccurrence, ...]
    issues: tuple[SourceIssue, ...]


def _ordered_issues(issues):
    return tuple(sorted(set(issues), key=lambda i: (i.lecture_file, i.code, i.locator, i.message)))


def _safe_reference(value):
    return (isinstance(value, str) and bool(value) and not Path(value).is_absolute()
            and "\\" not in value and all(p not in {"", ".", ".."} for p in value.split("/")))


@dataclass(frozen=True)
class SourceIndex:
    records: tuple[SourceRecord, ...]
    occurrences: tuple[SourceOccurrence, ...]
    issues: tuple[SourceIssue, ...]

    def find(self, concept_name: str, aliases: Iterable[str] = (), *,
             lecture_hashes: Mapping[str, str] | None = None,
             allowed_courses: AbstractSet[str] | None = None,
             kinds: tuple[str, ...] = ("structured", "candidate"),
             text_search: bool = False) -> SourceMatches:
        if not set(kinds) <= {"structured", "candidate", "text_line"} or (text_search and kinds != ("text_line",)):
            raise ValueError("Invalid occurrence query mode")
        names = {normalize_concept_key(n) for n in (concept_name, *aliases) if isinstance(n, str)} - {""}
        selected = {r.relative_path: r for r in self.records}
        issues = list(self.issues if lecture_hashes is None else
                      (i for i in self.issues if i.lecture_file in lecture_hashes))
        if lecture_hashes is not None:
            if not lecture_hashes:
                issues.append(SourceIssue("", "missing_source_scope", "", "No contributing lectures declared"))
            for reference, expected in lecture_hashes.items():
                code = ""
                if not _safe_reference(reference): code = "unsafe_source_path"
                elif not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected): code = "invalid_source_hash"
                elif reference not in selected:
                    if not any(i.lecture_file == reference for i in issues): code = "missing_source"
                elif selected[reference].sha256 != expected: code = "source_hash_mismatch"
                elif allowed_courses is not None and selected[reference].course not in allowed_courses: code = "source_course_mismatch"
                if code:
                    issues.append(SourceIssue(str(reference), code, "", "Declared source is not eligible"))
            bad = {i.lecture_file for i in issues}
            selected = {p: r for p, r in selected.items() if p in lecture_hashes and p not in bad}
        if allowed_courses is not None:
            selected = {p: r for p, r in selected.items() if r.course in allowed_courses}
        matches = []
        for o in self.occurrences:
            if o.source.relative_path not in selected or o.kind not in kinds or not names:
                continue
            identities = {o.canonical_key} if o.canonical_key else set(o.identities)
            if (text_search and any(n in normalize_concept_key(o.text) for n in names)) or (
                    not text_search and names.intersection(identities)):
                matches.append(o)
        return SourceMatches(tuple(matches), _ordered_issues(issues))


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse(raw):
    value = json.loads(raw, object_pairs_hook=_object)
    json.dumps(value, allow_nan=False)  # Includes non-finite numbers nested in optional fields.
    return value


def _strings(value, name, *, sequence=False):
    if sequence:
        if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
            raise ValueError(f"Invalid string list: {name}")
    elif not isinstance(value, str):
        raise ValueError(f"Invalid string: {name}")


def _validate(payload):
    if not isinstance(payload, dict): raise ValueError("Lecture must be an object")
    course = payload.get("course")
    if not isinstance(course, dict): raise ValueError("Invalid course metadata")
    for name in ("course_id", "course_name"): _strings(course.get(name, ""), name)
    if not (course.get("course_id", "").strip() or course.get("course_name", "").strip()):
        raise ValueError("Missing source course")
    _strings(payload.get("pdf", ""), "pdf")
    count = payload.get("page_count")
    if type(count) is not int or count <= 0: raise ValueError("Invalid source page count")
    pages = payload.get("pages")
    if not isinstance(pages, list): raise ValueError("Invalid page inventory")
    seen = set()
    for page in pages:
        if not isinstance(page, dict): raise ValueError("Invalid source page")
        number = page.get("page_number")
        if type(number) is not int or not 1 <= number <= count or number in seen:
            raise ValueError("Invalid/duplicate source page number")
        seen.add(number)
        for name in ("heading", "extracted_text"): _strings(page.get(name, ""), name)
        _strings(page.get("concept_candidates", []), "concept_candidates", sequence=True)
        if any(not normalize_concept_key(label) for label in page.get("concept_candidates", [])):
            raise ValueError("Missing candidate concept identity")
        items = page.get("concepts", [])
        if not isinstance(items, list): raise ValueError("Invalid structured concepts")
        for item in items:
            if not isinstance(item, dict): raise ValueError("Invalid structured concept")
            for name in ("concept_name", "concept_label", "name", "title", "canonical_key", "evidence",
                         "page_heading", "heading", "concept_type", "domain", "topic", "definition", "intuition",
                         "mathematical_foundation", "reason_for_inclusion", "reason"):
                _strings(item.get(name, ""), name)
            if not any(normalize_concept_key(item.get(name, "")) for name in
                       ("canonical_key", "concept_name", "concept_label", "name", "title")):
                raise ValueError("Missing structured concept identity")
            for name in ("aliases", "applications", "assumptions", "limitations", "advantages", "broader_topics",
                         "prerequisites", "related_concepts"):
                _strings(item.get(name, []), name, sequence=True)
            for name in ("importance_score", "confidence_score", "evidence_strength", "definition_quality_score", "interview_relevance"):
                if name in item and (type(item[name]) not in {int, float} or not math.isfinite(item[name])):
                    raise ValueError(f"Invalid numeric field: {name}")
            source = item.get("source", {})
            if not isinstance(source, dict): raise ValueError("Invalid item source")
            for name in ("page", "page_number"):
                if name in source and (type(source[name]) is not int or source[name] != number):
                    raise ValueError("Conflicting item source page")
            if "pdf" in source and source["pdf"] != payload.get("pdf", ""):
                raise ValueError("Conflicting item source PDF")


def _occurrences(record):
    def make(page, pointer, kind, labels=(), key="", text="", item=None, line=0, start=0, end=0):
        identity = {"policy": SOURCE_OCCURRENCE_POLICY_VERSION, "lecture_file": record.relative_path,
                    "lecture_sha256": record.sha256, "pointer": pointer, "line_number": line, "start": start, "end": end}
        digest = sha256(json.dumps(identity, sort_keys=True, ensure_ascii=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        return SourceOccurrence(digest, record, page['page_number'], pointer, kind, tuple(labels),
            normalize_concept_key(key), tuple(sorted({normalize_concept_key(n) for n in labels} - {""})),
            text, page.get('heading', ''), line, start, end, item if item is not None else MappingProxyType({}))
    for i, page in enumerate(record.payload['pages']):
        for j, item in enumerate(page.get('concepts', ())):
            labels = [item[n] for n in ('concept_name', 'concept_label', 'name', 'title') if item.get(n)]
            labels.extend(item.get('aliases', ()))
            yield make(page, f'/pages/{i}/concepts/{j}', 'structured', labels, item.get('canonical_key', ''), item.get('evidence', ''), item)
        for j, label in enumerate(page.get('concept_candidates', ())):
            yield make(page, f'/pages/{i}/concept_candidates/{j}', 'candidate', [label], text=label)
        start = 0
        for j, line in enumerate(page.get('extracted_text', '').splitlines(keepends=True), 1):
            text = line.rstrip('\r\n')
            yield make(page, f'/pages/{i}/extracted_text', 'text_line', text=text, line=j, start=start, end=start+len(text))
            start += len(line)


def index_sources(sources: Iterable[tuple[str, bytes]]) -> SourceIndex:
    grouped = {}
    for path, raw in sources:
        grouped.setdefault(path, set()).add(raw)
    records, occurrences, issues = [], [], []
    for reference in sorted(grouped):
        raws = grouped[reference]
        if not _safe_reference(reference):
            issues.append(SourceIssue(reference, 'unsafe_source_path', '', 'Unsafe relative lecture path'))
            continue
        if len(raws) != 1:
            issues.append(SourceIssue(reference, 'duplicate_source', '', 'Conflicting source bytes'))
            continue
        raw = next(iter(raws))
        try:
            payload = _parse(raw)
            _validate(payload)
            course = payload['course']
            record = SourceRecord(reference, sha256(raw).hexdigest(), raw, course.get('course_id', '').strip(),
                course.get('course_name', '').strip(), payload.get('pdf', ''), payload['page_count'], _freeze(payload))
            records.append(record)
            occurrences.extend(_occurrences(record))
        except (ValueError, TypeError, KeyError, OverflowError) as exc:
            issues.append(SourceIssue(reference, 'invalid_source', '', str(exc)))
    occurrences.sort(key=lambda o: (o.source.relative_path, o.page_number, o.json_pointer, o.line_number, o.start, o.end))
    return SourceIndex(tuple(records), tuple(occurrences), _ordered_issues(issues))


def load_source_index(processed_root: Path) -> SourceIndex:
    sources, issues = [], []
    if processed_root.is_symlink():
        return SourceIndex((), (), (SourceIssue('', 'unsafe_source_path', '', 'Symlink processed root'),))
    try:
        for path in sorted(processed_root.rglob('*')):
            relative = path.relative_to(processed_root).as_posix()
            if path.is_symlink():
                issues.append(SourceIssue(relative, 'unsafe_source_path', '', 'Symlink source path'))
            elif path.name == 'lecture.json':
                try: sources.append((relative, path.read_bytes()))
                except OSError as exc: issues.append(SourceIssue(relative, 'source_read_error', '', str(exc)))
    except OSError as exc:
        issues.append(SourceIssue('', 'source_read_error', '', str(exc)))
    index = index_sources(sources)
    return SourceIndex(index.records, index.occurrences, _ordered_issues((*index.issues, *issues)))
