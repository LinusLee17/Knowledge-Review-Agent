from __future__ import annotations

import json
import re
import os
from hashlib import sha256
from collections import Counter, defaultdict
from dataclasses import dataclass, field, fields, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from .concept_document import (
    REFERENCE_PATTERN, _lines as _document_lines, map_document_links, parse_concept_document,
)
from .concept_store import (
    concept_directory, load_concept_metadata, merge_concept_metadata,
    normalize_concept_metadata, write_concept_record, recover_concept_transactions,
    concept_history_root,
)
from .source_occurrences import SourceIndex, SourceIssue, SourceValidationError, index_sources, load_source_index
from .models import ConceptMetadata, PersistenceAlternative, PersistenceConflict
from .concept_rules import (
    canonical_candidate_label,
    canonical_common_mistakes_for_label,
    canonical_common_variants_for_label,
    canonical_connections_for_label,
    canonical_further_reading_for_label,
    canonical_how_it_works_for_label,
    canonical_interview_questions_for_label,
    canonical_intuition_for_label,
    canonical_key_components_for_label,
    canonical_advantages_for_label,
    canonical_assumptions_for_label,
    canonical_limitations_for_label,
    canonical_math_for_label,
    canonical_summary_for_label,
    canonical_why_it_matters_for_label,
    importance_for_label,
    profile_for_label,
    split_alias_and_application,
)
from .utils import canonical_concept_name, normalize_concept_key, normalize_lines, normalize_spaces, slugify


@dataclass(frozen=True)
class LectureArtifact:
    path: Path
    relative_path: str
    sha256: str
    payload: dict
    source_index: SourceIndex | None = None


@dataclass(frozen=True)
class ConceptMention:
    concept_label: str
    concept_key: str
    concept_type: str
    domain: str
    topic: str
    importance_score: int
    confidence_score: float
    evidence_strength: float
    definition_quality_score: float
    interview_relevance: float
    reason_for_inclusion: str
    definition: str
    intuition: str
    mathematical_foundation: str
    assumptions: list[str]
    applications: list[str]
    limitations: list[str]
    advantages: list[str]
    broader_topics: list[str]
    prerequisites: list[str]
    related_concepts: list[str]
    aliases: list[str]
    course_id: str
    course_name: str
    lecture_file: str
    lecture_hash: str
    source_pdf: str
    page_number: int
    page_heading: str
    evidence: str
    occurrence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class ConceptRecord:
    key: str
    directory: Path
    metadata_path: Path
    metadata: ConceptMetadata


@dataclass
class ConsolidationReport:
    created: list[str] = field(default_factory=list)
    updated: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)
    duplicate_dirs: list[str] = field(default_factory=list)
    total_mentions: int = 0


def _scope_label(scope_level: int) -> str:
    return {
        5: "broad family",
        4: "topic or workflow",
        3: "core concept or method",
        2: "supporting concept or practice",
        1: "specific metric or detail",
    }.get(int(scope_level or 3), "core concept or method")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def discover_lecture_artifacts(processed_root: Path) -> list[LectureArtifact]:
    index = load_source_index(processed_root)
    if index.issues:
        raise SourceValidationError(index.issues)
    return [LectureArtifact(processed_root / r.relative_path, r.relative_path, r.sha256,
                            json.loads(r.raw), index) for r in index.records]


def discover_concept_records(concepts_root: Path) -> list[ConceptRecord]:
    records: list[ConceptRecord] = []
    for metadata_path in sorted(concepts_root.rglob("metadata.json")):
        if not metadata_path.is_file():
            continue
        metadata = load_concept_metadata(metadata_path)
        if not metadata:
            continue
        directory = metadata_path.parent
        key = metadata.canonical_key or normalize_concept_key(metadata.concept_name)
        if not key:
            continue
        records.append(
            ConceptRecord(
                key=key,
                directory=directory,
                metadata_path=metadata_path,
                metadata=metadata,
            )
        )
    return records


def _lecture_course(payload: dict) -> tuple[str, str]:
    course = payload.get("course", {}) or {}
    return str(course.get("course_id", "") or ""), str(course.get("course_name", "") or "")


def _unique_text_list(values: Iterable[str]) -> list[str]:
    results: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = normalize_spaces(str(value or ""))
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append(text)
    return results


def _is_usable_field_fragment(value: str, field_name: str = "") -> bool:
    """Reject stale slide fragments and generated placeholder prose."""
    text = normalize_spaces(value)
    if not text:
        return False
    lowered = text.lower()
    if "extra topic if time permits" in lowered:
        return False
    if lowered.startswith(("page ", "slide ", "week ", "agenda", "introduction")):
        return False
    if lowered.startswith(("some limitations", "some advantages")):
        return False
    if lowered.startswith("use the metric definition from the confusion matrix"):
        return False
    if lowered.startswith("the mathematical form is") or lowered.startswith("the mathematical form follows"):
        return False
    if field_name in {"advantages", "limitations", "assumptions"} and lowered.endswith(
        (" there are", " there is", " are", " is", ":")
    ):
        return False
    if field_name == "assumptions" and re.match(r"^assumptions for .+ model$", lowered):
        return False
    if field_name == "applications" and lowered in {
        "used in examples",
        "used in this lecture",
        "used in the lecture",
        "examples",
    }:
        return False
    return len(text.split()) >= 2 or field_name not in {"advantages", "limitations", "assumptions"}


def _clean_field_list(values: Iterable[str], field_name: str = "") -> list[str]:
    return _unique_text_list(value for value in values if _is_usable_field_fragment(value, field_name))


def _clean_math(value: str) -> str:
    text = normalize_spaces(value)
    return text if _is_usable_field_fragment(text, "mathematical_foundation") else ""


def _usable_enrichment(text: str) -> bool:
    """Reject old placeholder prose from optional named rules."""
    lowered = normalize_spaces(text).lower()
    blocked = (
        "durable idea worth remembering",
        "repeatable procedure: start from the inputs",
        "apply the core rule",
        "core rule",
        "reusable building block",
        "language that makes the rest of the topic precise",
        "defines the objects, relationships, and assumptions",
        "nearby but different concept",
        "memorizing the name",
        "do not memorize",
    )
    return bool(lowered) and not any(fragment in lowered for fragment in blocked)


def _normalise_concept_source(item: dict, artifact: LectureArtifact, page_number: int, course_id: str, course_name: str) -> ConceptMention | None:
    raw_label = normalize_spaces(
        str(
            item.get("concept_name")
            or item.get("concept_label")
            or item.get("name")
            or item.get("title")
            or ""
        )
    )
    if not raw_label:
        return None

    base_label, application_suffixes = split_alias_and_application(raw_label)
    profile = profile_for_label(base_label)
    concept_label = profile.concept_name if profile else canonical_candidate_label(base_label)
    if not concept_label:
        return None

    concept_key = normalize_concept_key(item.get("canonical_key") or concept_label)
    if not concept_key:
        return None

    importance = int(item.get("importance_score", 1) or 1)
    if profile:
        importance = max(importance, profile.importance_score)
    if importance < 3 and not profile:
        return None

    source = item.get("source", {}) or {}
    source_pdf = normalize_spaces(str(source.get("pdf", "") or artifact.payload.get("pdf", "") or ""))
    page_heading = normalize_spaces(str(item.get("page_heading", "") or item.get("heading", "") or ""))
    evidence = normalize_spaces(str(item.get("evidence", "") or page_heading or ""))

    applications = _clean_field_list(
        [*(item.get("applications", []) or []), *application_suffixes, *(profile.applications if profile else [])],
        "applications",
    )
    prerequisites = _unique_text_list([*(item.get("prerequisites", []) or []), *(profile.prerequisites if profile else [])])
    related = _unique_text_list([*(item.get("related_concepts", []) or []), *(profile.related_concepts if profile else [])])
    broader_topics = _unique_text_list([*(item.get("broader_topics", []) or []), *(profile.broader_topics if profile else [])])
    aliases = _unique_text_list([raw_label, concept_label, *(item.get("aliases", []) or [])])

    return ConceptMention(
        concept_label=concept_label,
        concept_key=concept_key,
        concept_type=str(item.get("concept_type", "") or (profile.concept_type if profile else "")),
        domain=normalize_spaces(str(item.get("domain", "") or (profile.domain if profile else ""))),
        topic=normalize_spaces(str(item.get("topic", "") or (profile.topic if profile else ""))),
        importance_score=importance,
        confidence_score=float(item.get("confidence_score", 0.0) or 0.0),
        evidence_strength=float(item.get("evidence_strength", 0.0) or 0.0),
        definition_quality_score=float(item.get("definition_quality_score", 0.0) or 0.0),
        interview_relevance=float(item.get("interview_relevance", 0.0) or 0.0),
        reason_for_inclusion=str(item.get("reason_for_inclusion", "") or item.get("reason", "") or ""),
        definition=normalize_spaces(str(item.get("definition", "") or "")),
        intuition=normalize_spaces(str(item.get("intuition", "") or "")),
        mathematical_foundation=_clean_math(str(item.get("mathematical_foundation", "") or "")),
        assumptions=_clean_field_list(item.get("assumptions", []) or [], "assumptions"),
        applications=applications,
        limitations=_clean_field_list(item.get("limitations", []) or [], "limitations"),
        advantages=_clean_field_list(item.get("advantages", []) or [], "advantages"),
        broader_topics=broader_topics,
        prerequisites=prerequisites,
        related_concepts=related,
        aliases=aliases,
        course_id=course_id,
        course_name=course_name,
        lecture_file=artifact.relative_path,
        lecture_hash=artifact.sha256,
        source_pdf=source_pdf,
        page_number=page_number,
        page_heading=page_heading,
        evidence=evidence,
    )


def _fallback_mentions_from_candidates(
    artifact: LectureArtifact,
    page_number: int,
    heading: str,
    candidates: list[str],
    course_id: str,
    course_name: str,
) -> list[ConceptMention]:
    mentions: list[ConceptMention] = []
    seen: set[str] = set()
    for candidate in candidates:
        label = canonical_candidate_label(candidate)
        if not label:
            continue
        profile = profile_for_label(label)
        concept_label = profile.concept_name if profile else label
        concept_key = normalize_concept_key(concept_label)
        if not concept_key or concept_key in seen:
            continue
        seen.add(concept_key)
        importance = importance_for_label(concept_label, heading, course_name, 1)
        if importance < 3 and not profile:
            continue
        mentions.append(
            ConceptMention(
                concept_label=concept_label,
                concept_key=concept_key,
                concept_type=profile.concept_type if profile else "",
                domain=profile.domain if profile else "",
                topic=profile.topic if profile else "",
                importance_score=max(importance, profile.importance_score) if profile else importance,
                confidence_score=0.0,
                evidence_strength=0.0,
                definition_quality_score=0.0,
                interview_relevance=0.0,
                reason_for_inclusion="fallback candidate",
                # Heading alone is not a definition. Keep it as provenance
                # evidence so synthesis can flag weak pages for review.
                definition="",
                intuition="",
                mathematical_foundation="",
                assumptions=[],
                applications=list(profile.applications) if profile else [],
                limitations=[],
                advantages=[],
                broader_topics=list(profile.broader_topics) if profile else [],
                prerequisites=list(profile.prerequisites) if profile else [],
                related_concepts=list(profile.related_concepts) if profile else [],
                aliases=[label],
                course_id=course_id,
                course_name=course_name,
                lecture_file=artifact.relative_path,
                lecture_hash=artifact.sha256,
                source_pdf=str(artifact.payload.get("pdf", "") or ""),
                page_number=page_number,
                page_heading=heading,
                evidence=heading,
            )
        )
    return mentions


def _select_evidence(label: str, heading: str, lines: list[str]) -> str:
    normalized_label = normalize_concept_key(label)
    label_tokens = [token for token in normalized_label.split() if token]
    for line in lines:
        lowered = line.lower()
        if normalized_label and normalized_label in lowered:
            return line
        if label_tokens and all(token in lowered for token in label_tokens[:3]):
            return line
    if heading:
        return heading
    if lines:
        return lines[0]
    return label


def build_mentions(artifact: LectureArtifact) -> list[ConceptMention]:
    index = artifact.source_index
    if index is None:
        raw = artifact.path.read_bytes()
        if sha256(raw).hexdigest() != artifact.sha256:
            raise SourceValidationError((SourceIssue(artifact.relative_path, "source_hash_mismatch", "", "Artifact bytes changed"),))
        index = index_sources([(artifact.relative_path, raw)])
    if index.issues:
        raise SourceValidationError(index.issues)
    record = next(r for r in index.records if r.relative_path == artifact.relative_path)
    mentions = []
    positions = {}
    # Synthesis selection follows original array order, not lexical locator order.
    selected = (o for o in index.occurrences if o.source.relative_path == artifact.relative_path
                and o.kind in {"structured", "candidate"})
    selected = sorted(selected, key=lambda o: (int(o.json_pointer.split("/")[2]),
                                              int(o.json_pointer.split("/")[-1])))
    for occurrence in selected:
        page = record.payload["pages"][int(occurrence.json_pointer.split("/")[2])]
        heading = normalize_spaces(occurrence.page_heading)
        if occurrence.kind == "structured":
            mention = _normalise_concept_source(occurrence.item, artifact, occurrence.page_number,
                                               record.course_id, record.course_name)
            candidates = [mention] if mention else []
        elif not page.get("concepts"):
            candidates = _fallback_mentions_from_candidates(artifact, occurrence.page_number, heading,
                list(occurrence.labels), record.course_id, record.course_name)
        else:
            candidates = []
        for mention in candidates:
            evidence = normalize_spaces(mention.evidence or _select_evidence(mention.concept_label,
                heading, normalize_lines(page.get("extracted_text", ""))))
            key = (mention.concept_key, mention.page_number, evidence.lower())
            if key in positions:
                old = mentions[positions[key]]
                mentions[positions[key]] = replace(old, occurrence_ids=tuple(sorted(set(old.occurrence_ids) | {occurrence.occurrence_id})))
            else:
                positions[key] = len(mentions)
                mentions.append(replace(mention, evidence=evidence, occurrence_ids=(occurrence.occurrence_id,)))
    return mentions


def collect_mentions(artifacts: Iterable[LectureArtifact]) -> tuple[dict[str, list[ConceptMention]], dict[str, str]]:
    mentions_by_key: dict[str, list[ConceptMention]] = defaultdict(list)
    lecture_hashes: dict[str, str] = {}
    for artifact in artifacts:
        lecture_hashes[artifact.relative_path] = artifact.sha256
        for mention in build_mentions(artifact):
            mentions_by_key[mention.concept_key].append(mention)
    return mentions_by_key, lecture_hashes


def _choose_primary_record(records: list[ConceptRecord]) -> ConceptRecord:
    ordered = sorted(
        records,
        key=lambda record: (
            record.metadata.version_number,
            record.metadata.last_updated_timestamp,
            str(record.directory),
        ),
        reverse=True,
    )
    return ordered[0]


def _preferred_display_name(mentions: list[ConceptMention], fallback_key: str) -> str:
    if not mentions:
        return canonical_concept_name(fallback_key) or fallback_key
    counts = Counter(mention.concept_label for mention in mentions if mention.concept_label)
    if not counts:
        return canonical_concept_name(fallback_key) or fallback_key
    best_count = max(counts.values())
    best_labels = [label for label, count in counts.items() if count == best_count]
    best_labels.sort(key=lambda value: (len(value), value.lower()))
    return best_labels[0]


def _dedupe_text_fragments(mentions: list[ConceptMention]) -> list[str]:
    fragments: list[str] = []
    seen: set[str] = set()
    fields = (
        "definition",
        "intuition",
        "mathematical_foundation",
        "evidence",
    )
    list_fields = ("assumptions", "applications", "limitations", "advantages")

    for mention in mentions:
        for field_name in fields:
            text = normalize_spaces(getattr(mention, field_name, ""))
            if not text:
                continue
            for sentence in re.split(r"(?<=[.!?])\s+", text):
                sentence = normalize_spaces(sentence)
                if not sentence:
                    continue
                key = normalize_concept_key(sentence)
                if key in seen:
                    continue
                seen.add(key)
                fragments.append(sentence)
        for field_name in list_fields:
            for item in getattr(mention, field_name, []) or []:
                text = normalize_spaces(item)
                if not text:
                    continue
                key = normalize_concept_key(text)
                if key in seen:
                    continue
                seen.add(key)
                fragments.append(text)
    return fragments


def _merged_text_block(mentions: list[ConceptMention], attr: str) -> str:
    fragments: list[str] = []
    seen: set[str] = set()
    for mention in mentions:
        text = normalize_spaces(getattr(mention, attr, ""))
        if not text:
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            sentence = normalize_spaces(sentence)
            if not sentence:
                continue
            key = normalize_concept_key(sentence)
            if key in seen:
                continue
            seen.add(key)
            fragments.append(sentence)
    return " ".join(fragments[:4]).strip()


def _page_range_text(page_numbers: list[int]) -> str:
    if not page_numbers:
        return ""
    pages = sorted({int(page) for page in page_numbers if int(page) > 0})
    if not pages:
        return ""
    ranges: list[tuple[int, int]] = []
    start = end = pages[0]
    for page in pages[1:]:
        if page == end + 1:
            end = page
            continue
        ranges.append((start, end))
        start = end = page
    ranges.append((start, end))
    parts = [f"p{a}" if a == b else f"p{a}-p{b}" for a, b in ranges]
    return ", ".join(parts)


def _page_range_link_target(page_numbers: list[int], source_pdf: str) -> str:
    pages = sorted({int(page) for page in page_numbers if int(page) > 0})
    if not pages or not source_pdf:
        return ""
    first_page = pages[0]
    pdf_path = source_pdf.replace("\\", "/")
    if not pdf_path.startswith("../"):
        pdf_path = f"../data/raw/{pdf_path}"
    return f"{pdf_path}#page={first_page}"


def _markdown_link(label: str, target: str) -> str:
    safe_label = label.replace("[", "\\[").replace("]", "\\]")
    return f"[{safe_label}]({target})"


def _grouped_source_mentions(mentions: list[ConceptMention]) -> list[tuple[str, str, str, str, list[int]]]:
    grouped: dict[tuple[str, str, str, str], list[int]] = {}
    for mention in mentions:
        source_id = mention.course_id or mention.course_name or "unknown course"
        lecture_file = mention.lecture_file or ""
        source_pdf = mention.source_pdf or ""
        evidence = normalize_spaces(mention.evidence or mention.definition or mention.page_heading)
        key = (source_id, lecture_file, source_pdf, evidence)
        grouped.setdefault(key, []).append(int(mention.page_number or 0))
    ordered = sorted(
        grouped.items(),
        key=lambda item: (
            item[0][0].lower(),
            item[0][1].lower(),
            min((page for page in item[1] if page > 0), default=0),
            item[0][3].lower(),
        ),
    )
    return [(source_id, lecture_file, source_pdf, evidence, pages) for (source_id, lecture_file, source_pdf, evidence), pages in ordered]


def _slide_evidence_lines(mentions: list[ConceptMention], limit: int = 5) -> list[str]:
    lines: list[str] = []
    for source_id, lecture_file, _source_pdf, evidence, pages in _grouped_source_mentions(mentions):
        if not evidence:
            continue
        page_text = _page_range_text(pages)
        parts = [f"- {source_id}"]
        if page_text:
            parts.append(page_text)
        if _source_pdf:
            pdf_label = _source_pdf.split("/")[-1]
            pdf_target = _page_range_link_target(pages, _source_pdf)
            if pdf_target:
                parts.append(_markdown_link(pdf_label, pdf_target))
            else:
                parts.append(f"`{pdf_label}`")
        line = " | ".join(parts) + f" — {evidence}"
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


def _explanation_basis(concept_name: str) -> str:
    return "slide evidence + background synthesis" if canonical_summary_for_label(concept_name) else "slide evidence"


def _synthesized_definition(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    summary = canonical_summary_for_label(concept_name)
    if _usable_enrichment(summary):
        return summary

    fallback = _merged_text_block(mentions, "definition")
    if _usable_enrichment(fallback) and normalize_concept_key(fallback) != normalize_concept_key(concept_name):
        return fallback

    profile = profile_for_label(concept_name)
    concept_type = (metadata.concept_type or (profile.concept_type if profile else "concept")).lower()
    domain = metadata.domain or (profile.domain if profile else "")
    topic = metadata.topic or (profile.topic if profile else "")
    applications = metadata.applications or _merged_text_list(mentions, "applications")

    # Generic enrichment. Uses semantic slots, not concept-name cases. Named
    # profiles may improve wording, but weak profiles must never create filler.
    type_nouns = {
        "workflow": "repeatable workflow",
        "algorithm": "algorithm",
        "model": "model",
        "method": "method",
        "metric": "metric",
        "theory": "theory",
        "theorem": "theorem",
        "principle": "principle",
        "framework": "framework",
        "process": "process",
        "practice": "practice",
    }
    noun = type_nouns.get(concept_type, "concept")
    context = f" in {domain}" if domain else ""
    focus = f" for {topic}" if topic else ""
    purpose = ""
    if applications:
        purpose = f" It supports {', '.join(applications[:3])}."
    elif mentions and any(mention.evidence for mention in mentions):
        purpose = " Its exact purpose should be read with the source evidence below."
    return f"{concept_name} is a {noun}{context}{focus}.{purpose}"

    return f"{concept_name} is a durable knowledge concept relevant to the course material."


def _synthesized_intuition(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    intuition = canonical_intuition_for_label(concept_name)
    if _usable_enrichment(intuition):
        return intuition
    if _usable_enrichment(metadata.intuition):
        return metadata.intuition
    fallback = _merged_text_block(mentions, "intuition")
    if fallback:
        return fallback
    concept_type = (metadata.concept_type or "concept").lower()
    applications = metadata.applications or _merged_text_list(mentions, "applications")
    if concept_type == "workflow":
        return "Mental model: inspect evidence, choose next action, then validate what changed." + (
            f" Goal: {', '.join(applications[:2])}." if applications else ""
        )
    if concept_type in {"algorithm", "method", "process"}:
        return "Mental model: transform inputs through explicit steps until output meets its evaluation rule."
    if concept_type == "metric":
        return "Mental model: compress one aspect of performance or uncertainty into a number; interpretation depends on its denominator and context."
    if concept_type in {"model", "theory", "framework", "principle", "theorem"}:
        return "Mental model: use stated assumptions to connect observable inputs with conclusions or decisions."
    return "Mental model: identify the object, its role, and the evidence needed to use it correctly."


def _synthesized_math(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    math = canonical_math_for_label(concept_name)
    if math:
        return math
    if metadata.mathematical_foundation:
        return _clean_math(metadata.mathematical_foundation)
    fallback = _merged_text_block(mentions, "mathematical_foundation")
    return _clean_math(fallback)


def _further_reading(concept_name: str) -> list[str]:
    return canonical_further_reading_for_label(concept_name)


def _why_it_matters(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    text = canonical_why_it_matters_for_label(concept_name)
    if _usable_enrichment(text):
        return text
    applications = metadata.applications or _merged_text_list(mentions, "applications")
    related = metadata.related_concepts or _merged_text_list(mentions, "related_concepts")
    if applications:
        concept_type = (metadata.concept_type or "concept").lower()
        if concept_type == "workflow":
            return f"{concept_name} turns observations into evidence for {', '.join(applications[:3])}, helping decide what to investigate or model next."
        if concept_type == "metric":
            return f"{concept_name} makes {', '.join(applications[:3])} measurable, so alternatives can be compared against an explicit quantity."
        if concept_type in {"model", "algorithm", "method", "theory", "theorem"}:
            return f"{concept_name} provides a formal way to support {', '.join(applications[:3])} under stated assumptions."
        return (
            f"{concept_name} matters because it supports {', '.join(applications[:3])} with an explicit concept and evidence trail."
        )
    if related:
        return f"{concept_name} matters because it connects to {', '.join(related[:3])} and helps organize the topic."
    if metadata.domain or metadata.topic:
        return f"{concept_name} matters because it is a durable concept in {metadata.domain or 'the target domain'}."
    return ""


def _how_it_works(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    text = canonical_how_it_works_for_label(concept_name)
    if _usable_enrichment(text):
        return text
    concept_type = (metadata.concept_type or "concept").lower()
    prerequisites = metadata.prerequisites or _merged_text_list(mentions, "prerequisites")
    applications = metadata.applications or _merged_text_list(mentions, "applications")
    related = metadata.related_concepts or _merged_text_list(mentions, "related_concepts")
    steps: list[str] = []
    if concept_type == "workflow":
        steps = ["1. Define question, objective, or decision.", "2. Inspect relevant evidence and identify signal, uncertainty, or failure.", "3. Apply suitable analysis steps.", "4. Validate findings before acting."]
    elif concept_type in {"algorithm", "method", "process", "practice"}:
        steps = ["1. Specify inputs and objective.", "2. Apply method steps under stated assumptions.", "3. Produce output, estimate, or decision.", "4. Evaluate output against an explicit criterion."]
    elif concept_type == "metric":
        steps = ["1. Define quantity and population being measured.", "2. Compute metric from observed outcomes.", "3. Interpret value with scale, denominator, and decision context."]
    elif concept_type in {"model", "theory", "framework", "principle", "theorem"}:
        steps = ["1. State objects and assumptions.", "2. Apply governing relationship or rule.", "3. Derive result or prediction.", "4. Check fit, limitations, and downstream decision use."]
    else:
        steps = ["1. Identify object and intended question.", "2. Apply definition under its assumptions.", "3. Compare result with related concepts and evidence."]
    if prerequisites:
        steps.insert(0, f"Prerequisites: {', '.join(prerequisites[:4])}.")
    if applications:
        steps.append(f"Typical use context: {', '.join(applications[:3])}.")
    if related:
        steps.append(f"Compare against: {', '.join(related[:3])}.")
    return "\n".join(steps)


def _key_components(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    components = canonical_key_components_for_label(concept_name)
    if components and not any(not _usable_enrichment(item) for item in components):
        return components
    components: list[str] = []
    if metadata.prerequisites:
        components.append(f"Prerequisites: {', '.join(metadata.prerequisites[:4])}")
    if metadata.assumptions:
        components.append(f"Assumptions: {', '.join(metadata.assumptions[:4])}")
    if metadata.applications:
        components.append(f"Decision/use context: {', '.join(metadata.applications[:4])}")
    if metadata.related_concepts:
        components.append(f"Neighbor concepts: {', '.join(metadata.related_concepts[:4])}")
    return components


def _common_variants(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    # Aliases belong in Classification. Do not present them as variants.
    return canonical_common_variants_for_label(concept_name)


def _common_mistakes(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    mistakes = canonical_common_mistakes_for_label(concept_name)
    if mistakes and all(_usable_enrichment(item) for item in mistakes):
        return mistakes
    items: list[str] = []
    if metadata.limitations:
        items.extend(metadata.limitations[:3])
    if not items:
        items.append(f"Do not memorize {concept_name} without understanding its role in the surrounding topic.")
    return _unique_text_list(items)


def _interview_questions(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    questions = canonical_interview_questions_for_label(concept_name)
    generic_questions = (
        f"what problem does {concept_name.lower()} solve?",
        f"how does {concept_name.lower()} work at a high level?",
        f"when would you use {concept_name.lower()}, and when would you avoid it?",
    )
    if questions and not any(normalize_spaces(item).lower().startswith(generic) for item in questions for generic in generic_questions):
        return questions
    concept_type = (metadata.concept_type or "concept").lower()
    fallback = [
        f"What problem does {concept_name} solve, and what is its output?",
        f"Explain {concept_name} using one concrete input-to-decision example.",
        f"What assumptions must hold before using {concept_name}?",
        f"Which trade-off decides whether to use {concept_name} instead of an alternative?",
    ]
    if concept_type == "metric":
        fallback.insert(2, f"What does the denominator of {concept_name} include or exclude?")
    elif concept_type in {"algorithm", "method", "workflow", "process"}:
        fallback.insert(2, f"Walk through {concept_name} step by step and name its stopping or evaluation rule.")
    related = metadata.related_concepts or _merged_text_list(mentions, "related_concepts")
    if related:
        fallback.append(f"How does {concept_name} compare with {related[0]}?")
    return fallback


def _connections(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    connections = canonical_connections_for_label(concept_name)
    if connections:
        return connections
    lines: list[str] = []
    prerequisites = metadata.prerequisites or _merged_text_list(mentions, "prerequisites")
    related = metadata.related_concepts or _merged_text_list(mentions, "related_concepts")
    applications = metadata.applications or _merged_text_list(mentions, "applications")
    broader_topics = metadata.broader_topics or _merged_text_list(mentions, "broader_topics")
    if prerequisites:
        lines.append(f"Depends on: {', '.join(prerequisites[:4])}")
    if applications:
        lines.append(f"Used in: {', '.join(applications[:4])}")
    if related:
        lines.append(f"Related: {', '.join(related[:4])}")
    if broader_topics:
        lines.append(f"Broader topic: {', '.join(broader_topics[:4])}")
    return lines


def _quality_review_flags(
    metadata: ConceptMetadata,
    mentions: list[ConceptMention],
    definition: str,
    mathematical_foundation: str,
    key_components: list[str],
    assumptions: list[str],
    limitations: list[str],
    applications: list[str],
) -> list[str]:
    """Expose missing evidence instead of hiding it behind generic prose."""
    flags: list[str] = []
    source_evidence = [mention.evidence for mention in mentions if normalize_spaces(mention.evidence)]
    if not definition or len(definition.split()) < 12:
        flags.append("definition lacks specific object, purpose, or scope")
    if not source_evidence or all(normalize_concept_key(item) == normalize_concept_key(metadata.concept_name) for item in source_evidence):
        flags.append("source evidence is too thin for a concrete explanation")
    if metadata.concept_type in {"workflow", "algorithm", "method", "process"} and not key_components:
        flags.append("workflow/method components not supported by extracted evidence")
    if metadata.concept_type in {"model", "metric", "theory", "theorem"} and not mathematical_foundation:
        flags.append("no meaningful equation or formal relationship extracted")
    if not assumptions:
        flags.append("assumptions not extracted")
    if not limitations:
        flags.append("trade-offs or limitations not extracted")
    if not applications:
        flags.append("real-world application not extracted")
    return flags


def _merged_text_list(mentions: list[ConceptMention], attr: str) -> list[str]:
    items: list[str] = []
    for mention in mentions:
        items.extend(getattr(mention, attr, []) or [])
    return _unique_text_list(items)


def _provenance_lines(metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    lines: list[str] = []
    mention_lecture_files = {mention.lecture_file for mention in mentions}

    for source_id, lecture_file, source_pdf, evidence, pages in _grouped_source_mentions(mentions):
        page_text = _page_range_text(pages)
        parts = [f"- {source_id}"]
        if page_text:
            parts.append(page_text)
        if source_pdf:
            pdf_label = source_pdf.split("/")[-1]
            pdf_target = _page_range_link_target(pages, source_pdf)
            if pdf_target:
                parts.append(_markdown_link(pdf_label, pdf_target))
            else:
                parts.append(f"`{pdf_label}`")
        line = " | ".join(parts)
        if evidence:
            line += f" — {evidence}"
        lines.append(line)

    for lecture_file in metadata.contributing_lecture_files:
        if lecture_file in mention_lecture_files:
            continue
        hash_value = metadata.source_lecture_hashes.get(lecture_file, "")
        line = f"- `{lecture_file}`"
        if hash_value:
            line += f" | `{hash_value}`"
        lines.append(line)

    if not lines:
        lines.append(f"- provenance preserved from {len(metadata.contributing_lecture_files)} lecture file(s)")

    return lines


def build_concept_markdown(
    concept_name: str,
    canonical_key: str,
    metadata: ConceptMetadata,
    mentions: list[ConceptMention],
) -> str:
    definition = metadata.definition or _synthesized_definition(concept_name, metadata, mentions)
    why_it_matters = _why_it_matters(concept_name, metadata, mentions)
    intuition = metadata.intuition or _synthesized_intuition(concept_name, metadata, mentions)
    how_it_works = _how_it_works(concept_name, metadata, mentions)
    mathematical_foundation = metadata.mathematical_foundation or _synthesized_math(concept_name, metadata, mentions)
    key_components = _key_components(concept_name, metadata, mentions)
    assumptions = metadata.assumptions or _merged_text_list(mentions, "assumptions")
    advantages = metadata.advantages or _merged_text_list(mentions, "advantages")
    applications = metadata.applications or _merged_text_list(mentions, "applications")
    limitations = metadata.limitations or _merged_text_list(mentions, "limitations")
    common_variants = _common_variants(concept_name, metadata, mentions)
    common_mistakes = _common_mistakes(concept_name, metadata, mentions)
    broader_topics_raw = metadata.broader_topics or _merged_text_list(mentions, "broader_topics")
    blocked_broader_topics = {
        normalize_concept_key(concept_name),
        normalize_concept_key(metadata.domain),
        normalize_concept_key(metadata.topic),
        normalize_concept_key("foundations"),
    }
    broader_topics = [
        item
        for item in broader_topics_raw
        if normalize_concept_key(item) not in blocked_broader_topics
    ]
    alias_candidates = metadata.aliases or _merged_text_list(mentions, "aliases")
    variant_keys = {normalize_concept_key(item) for item in common_variants}
    aliases = [
        alias
        for alias in alias_candidates
        if normalize_concept_key(alias) != normalize_concept_key(concept_name)
        and normalize_concept_key(alias) not in variant_keys
    ]
    if not aliases:
        aliases = [alias for alias in alias_candidates if normalize_concept_key(alias) != normalize_concept_key(concept_name)]
    interview_questions = _interview_questions(concept_name, metadata, mentions)
    further_reading = _further_reading(concept_name)
    connections = _connections(concept_name, metadata, mentions)
    slide_evidence = _slide_evidence_lines(mentions)
    review_flags = _quality_review_flags(metadata, mentions, definition, mathematical_foundation, key_components, assumptions, limitations, applications)

    lines = [
        "---",
        f'concept_name: "{concept_name}"',
        f'canonical_key: "{canonical_key}"',
        f'concept_type: "{getattr(metadata, "concept_type", "")}"',
        f'domain: "{metadata.domain}"',
        f'topic: "{metadata.topic}"',
        f"importance_score: {metadata.importance_score}",
        f"scope_level: {metadata.scope_level}",
        f"study_priority: {metadata.study_priority}",
        f"version_number: {metadata.version_number}",
        f'last_updated_timestamp: "{metadata.last_updated_timestamp}"',
        f'explanation_basis: "{_explanation_basis(concept_name)}"',
        "---",
        "",
        f"# {concept_name}",
        "",
        "## Classification",
        f"- domain: {metadata.domain or 'unknown'}",
        f"- topic: {metadata.topic or 'unknown'}",
        f"- type: {getattr(metadata, 'concept_type', '') or 'unknown'}",
        f"- scope: {metadata.scope_level}/5 ({_scope_label(metadata.scope_level)})",
        f"- study priority: {metadata.study_priority}/5",
    ]

    if aliases:
        lines.append(f"- also known as: {', '.join(aliases[:5])}")
    if broader_topics:
        lines.append(f"- broader topic(s): {', '.join(broader_topics[:3])}")

    lines.extend(["", "## Contributing Courses"])
    if metadata.contributing_courses:
        for course in metadata.contributing_courses:
            lines.append(f"- {course}")
    else:
        lines.append("- unknown")

    if definition:
        lines.extend(["", "## Definition", definition])
    if why_it_matters:
        lines.extend(["", "## Why it Matters", why_it_matters])
    if intuition:
        lines.extend(["", "## Core Intuition", intuition])
    if how_it_works:
        lines.extend(["", "## How it Works"])
        lines.extend(how_it_works.splitlines())
    if mathematical_foundation:
        lines.extend(["", "## Mathematical Foundation", mathematical_foundation])
    if key_components:
        lines.extend(["", "## Key Components"])
        for item in key_components:
            lines.append(f"- {item}")

    if assumptions:
        lines.extend(["", "## Assumptions"])
        for item in assumptions:
            lines.append(f"- {item}")
    if advantages:
        lines.extend(["", "## Advantages"])
        for item in advantages:
            lines.append(f"- {item}")
    if limitations:
        lines.extend(["", "## Limitations"])
        for item in limitations:
            lines.append(f"- {item}")
    if common_mistakes:
        lines.extend(["", "## Common Mistakes"])
        for item in common_mistakes:
            lines.append(f"- {item}")
    if common_variants:
        lines.extend(["", "## Common Variants"])
        for item in common_variants:
            lines.append(f"- {item}")
    if applications:
        lines.extend(["", "## Real-world applications"])
        for item in applications:
            lines.append(f"- {item}")
    if interview_questions:
        lines.extend(["", "## Interview Questions"])
        for question in interview_questions:
            lines.append(f"- {question}")

    if metadata.related_concepts:
        lines.extend(["", "## Related Concepts"])
        for related in metadata.related_concepts:
            lines.append(f"- {related}")

    if connections:
        lines.extend(["", "## Connections"])
        for item in connections:
            lines.append(f"- {item}")

    if metadata.prerequisites:
        lines.extend(["", "## Prerequisites"])
        for prerequisite in metadata.prerequisites:
            lines.append(f"- {prerequisite}")

    if further_reading:
        lines.extend(["", "## Further Reading"])
        for item in further_reading:
            lines.append(f"- {item}")

    if slide_evidence:
        lines.extend(["", "## Slide-derived Evidence"])
        lines.extend(slide_evidence)

    lines.extend(["", "## Provenance"])
    lines.extend(_provenance_lines(metadata, mentions))

    if getattr(metadata, "confidence_score", None) is not None:
        lines.extend(
            [
                "",
                "## Extraction Metadata",
                f"- explanation basis: {_explanation_basis(concept_name)}",
                f"- confidence: {getattr(metadata, 'confidence_score', 0.0)}",
                f"- evidence strength: {getattr(metadata, 'evidence_strength', 0.0)}",
                f"- definition quality: {getattr(metadata, 'definition_quality_score', 0.0)}",
                f"- interview relevance: {getattr(metadata, 'interview_relevance', 0.0)}",
            ]
        )
        if metadata.version_number:
            lines.append(f"- version: {metadata.version_number}")
        if metadata.last_updated_timestamp:
            lines.append(f"- last updated: {metadata.last_updated_timestamp}")

    if review_flags:
        lines.extend(["", "## Quality Review"])
        lines.append("- This page needs human review before treated as authoritative:")
        lines.extend(f"- {flag}" for flag in review_flags)

    return "\n".join(lines).rstrip() + "\n"


def _merge_metadata(
    concept_name: str,
    canonical_key: str,
    mentions: list[ConceptMention],
    existing: ConceptMetadata | None,
) -> ConceptMetadata:
    course_names = [mention.course_id or mention.course_name for mention in mentions if (mention.course_id or mention.course_name)]
    lecture_files = [mention.lecture_file for mention in mentions]
    lecture_hashes = {mention.lecture_file: mention.lecture_hash for mention in mentions}
    now = datetime.now(timezone.utc).isoformat()

    def _best_text(attr: str, fallback: str = "") -> str:
        values = [normalize_spaces(getattr(mention, attr, "")) for mention in mentions]
        values = [value for value in values if value]
        if existing:
            existing_value = normalize_spaces(getattr(existing, attr, ""))
            if existing_value:
                values.append(existing_value)
        if not values:
            return fallback
        counts = Counter(values)
        best_count = max(counts.values())
        candidates = [value for value, count in counts.items() if count == best_count]
        candidates.sort(key=lambda value: (-len(value), value.lower()))
        return candidates[0]

    def _merged_list(attr: str) -> list[str]:
        values: list[str] = []
        if existing:
            values.extend(getattr(existing, attr, []) or [])
        for mention in mentions:
            values.extend(getattr(mention, attr, []) or [])
        return _clean_field_list(values, attr)

    if existing:
        if not mentions:
            return existing
        incoming = _merge_metadata(concept_name, canonical_key, mentions, None)
        values = {}
        conflicts = {conflict.field_name: conflict for conflict in existing.persistence_conflicts}
        for name in ("definition", "mathematical_foundation"):
            prior = getattr(existing, name)
            if not prior:
                continue
            conflict = conflicts.get(name)
            alternatives = set(conflict.alternatives if conflict else [])
            for mention in mentions:
                current = getattr(mention, name)
                if not current or normalize_spaces(current) == normalize_spaces(prior):
                    continue
                # Lecture alternatives refer to immutable source identities, not concept snapshots.
                reference = (f"lecture:{mention.lecture_file}#page={mention.page_number}"
                             f"&occurrences={','.join(sorted(mention.occurrence_ids))}")
                alternatives.add(PersistenceAlternative(reference, mention.lecture_hash, current))
            if alternatives:
                conflicts[name] = PersistenceConflict(name, prior, sorted(alternatives, key=lambda a: (
                    a.source_record, a.record_sha256, a.value, a.snapshot_id,
                )))
        for spec in fields(existing):
            name = spec.name
            prior, current = getattr(existing, name), getattr(incoming, name)
            if name == "persistence_conflicts":
                continue
            if isinstance(prior, list):
                values[name] = sorted(set(prior + current))
            elif isinstance(prior, dict):
                values[name] = {**prior, **current}
            elif isinstance(prior, str) and name != "last_updated_timestamp":
                values[name] = prior or current
        values["persistence_conflicts"] = [conflicts[name] for name in sorted(conflicts)]
        return normalize_concept_metadata(replace(existing, **values))

    merged_assumptions = canonical_assumptions_for_label(concept_name) or _merged_list("assumptions")
    merged_applications = _merged_list("applications")
    merged_limitations = canonical_limitations_for_label(concept_name) or _merged_list("limitations")
    merged_advantages = canonical_advantages_for_label(concept_name) or _merged_list("advantages")
    merged_broader_topics = _merged_list("broader_topics")
    merged_aliases = _merged_list("aliases")
    merged_related = _merged_list("related_concepts")
    merged_prereqs = _merged_list("prerequisites")
    merged_used_in = _merged_list("used_in")
    merged_domain = _best_text("domain")
    merged_topic = _best_text("topic")
    merged_definition = _best_text("definition")
    merged_intuition = _best_text("intuition")
    merged_math = _clean_math(_best_text("mathematical_foundation"))
    merged_importance = max([mention.importance_score for mention in mentions], default=1)
    merged_concept_type = _best_text("concept_type")
    merged_confidence_score = max([getattr(mention, "confidence_score", 0.0) for mention in mentions], default=0.0)
    merged_evidence_strength = max([getattr(mention, "evidence_strength", 0.0) for mention in mentions], default=0.0)
    merged_definition_quality_score = max([getattr(mention, "definition_quality_score", 0.0) for mention in mentions], default=0.0)
    merged_interview_relevance = max([getattr(mention, "interview_relevance", 0.0) for mention in mentions], default=0.0)
    preview_metadata = ConceptMetadata(
        concept_name=concept_name,
        canonical_key=canonical_key,
        concept_type=merged_concept_type,
        domain=merged_domain,
        topic=merged_topic,
        importance_score=merged_importance,
        applications=merged_applications,
        limitations=merged_limitations,
        assumptions=merged_assumptions,
        advantages=merged_advantages,
        broader_topics=merged_broader_topics,
        aliases=merged_aliases,
        contributing_courses=sorted(set(course_names)),
        contributing_lecture_files=sorted(set(lecture_files)),
        source_lecture_hashes=lecture_hashes,
        last_updated_timestamp=now,
        version_number=1,
        related_concepts=merged_related,
        prerequisites=merged_prereqs,
        used_in=[],
        graph_node_id=slugify(canonical_key),
    )
    merged_definition = _synthesized_definition(concept_name, preview_metadata, mentions)
    merged_intuition = _synthesized_intuition(concept_name, preview_metadata, mentions)
    merged_math = _synthesized_math(concept_name, preview_metadata, mentions)

    return ConceptMetadata(
        concept_name=concept_name,
        canonical_key=canonical_key,
        concept_type=merged_concept_type,
        domain=merged_domain,
        topic=merged_topic,
        importance_score=merged_importance,
        confidence_score=merged_confidence_score,
        evidence_strength=merged_evidence_strength,
        definition_quality_score=merged_definition_quality_score,
        interview_relevance=merged_interview_relevance,
        definition=merged_definition,
        intuition=merged_intuition,
        mathematical_foundation=merged_math,
        assumptions=merged_assumptions,
        applications=merged_applications,
        limitations=merged_limitations,
        advantages=merged_advantages,
        broader_topics=merged_broader_topics,
        aliases=merged_aliases,
        contributing_courses=sorted(set(course_names)),
        contributing_lecture_files=sorted(set(lecture_files)),
        source_lecture_hashes=lecture_hashes,
        last_updated_timestamp=now,
        version_number=1,
        related_concepts=merged_related,
        prerequisites=merged_prereqs,
        used_in=[],
        graph_node_id=slugify(canonical_key),
    )


def _page_sections(markdown: str) -> list[tuple[str, str]]:
    return [(section.heading, section.content.strip("\n"))
            for section in parse_concept_document(markdown).sections]


def _reference_text_parts(markdown: str) -> list[tuple[str, bool]]:
    """Keep fenced blocks and front matter outside reference rewriting."""
    runs: list[tuple[str, bool]] = []
    for line, visible in _document_lines(markdown):
        if runs and runs[-1][1] == visible:
            runs[-1] = (runs[-1][0] + line, visible)
        else:
            runs.append((line, visible))
    return runs


def _mask_reference_code(text: str) -> tuple[str, dict[str, str]]:
    """Mask code without cutting outer link/image labels into separate parser inputs."""
    replacements = {}
    def mask(match):
        token = "KRA_CODE_" + sha256(f"{len(replacements)}\n{match[0]}".encode()).hexdigest()
        while token in text or token in replacements:
            token += "_CODE"
        replacements[token] = match[0]
        return token
    return re.sub(r"(?<!`)(`+)(?!`)[\s\S]*?(?<!`)\1(?!`)", mask, text), replacements


def _restore_reference_code(text: str, replacements: dict[str, str]) -> str:
    for token, original in replacements.items():
        text = text.replace(token, original)
    return text


def _source_reference_definitions(markdown: str) -> dict[str, tuple[str, str]]:
    definitions = {}
    for text, visible in _reference_text_parts(markdown):
        if not visible:
            continue
        masked, codes = _mask_reference_code(text)
        for line in masked.splitlines(keepends=True):
            match = REFERENCE_PATTERN.match(line)
            if match:
                label = match[1].split("[", 1)[1].rsplit("]", 1)[0]
                definitions.setdefault(normalize_spaces(label).casefold(),
                    (label, _restore_reference_code(match[2], codes)))
    return definitions


def _namespace_reference_uses(text: str, labels: dict[str, str]) -> str:
    result = []
    index = 0
    while index < len(text):
        if text[index] == "\\":
            result.append(text[index:index + 2])
            index += 2
            continue
        if text[index] != "[":
            result.append(text[index])
            index += 1
            continue
        end, depth = index + 1, 1
        while end < len(text) and depth:
            if text[end] == "\\":
                end += 2
                continue
            depth += (text[end] == "[") - (text[end] == "]")
            end += 1
        if depth:
            result.append(text[index:])
            break
        label = text[index + 1:end - 1]
        rendered = "[" + _namespace_reference_uses(label, labels) + "]"
        suffix = re.match(r"[ \t]*\[([^\]\n]*)\]", text[end:])
        if suffix:
            key = normalize_spaces(suffix[1] or label).casefold()
            replacement = labels.get(key)
            result.append(rendered + (f"[{replacement}]" if replacement else suffix[0]))
            index = end + suffix.end()
        elif text[end:end + 1] == "(":
            # Leave inline destinations/titles opaque, including bracket-shaped URL text.
            stop, depth, quote_mark, angle = end + 1, 1, "", False
            while stop < len(text) and depth:
                char = text[stop]
                if char == "\\":
                    stop += 2
                    continue
                if quote_mark:
                    if char == quote_mark:
                        quote_mark = ""
                elif angle:
                    angle = char != ">"
                elif char == "<":
                    angle = True
                elif char in "\"'" and text[stop - 1].isspace():
                    quote_mark = char
                else:
                    depth += (char == "(") - (char == ")")
                stop += 1
            result.append(rendered + text[end:stop])
            index = stop
        else:
            replacement = labels.get(normalize_spaces(label).casefold())
            result.append(rendered + (f"[{replacement}]" if replacement else ""))
            index = end
    return "".join(result)


def _isolate_source_references(originals: dict[str, str]) -> dict[str, str]:
    """Namespace document-local labels before source documents share one Markdown scope."""
    parts = {origin: _reference_text_parts(text) for origin, text in originals.items()}
    definitions = {origin: _source_reference_definitions(text) for origin, text in originals.items()}
    counts = Counter(label for labels in definitions.values() for label in labels)
    reserved = set(counts)
    result = {}
    for origin, chunks in parts.items():
        document = parse_concept_document(originals[origin])
        skipped = {"classification", "contributing courses", "extraction metadata", "quality review"}
        dropped = _source_reference_definitions(document.prefix)
        for section in document.sections:
            if section.heading.lower() in skipped:
                dropped.update(_source_reference_definitions(section.content))
        hoist = set(dropped)
        labels = {}
        for label in sorted(definitions[origin]):
            if counts[label] < 2:
                continue
            candidate = "kra-ref-" + sha256(f"{origin}\n{label}".encode()).hexdigest()
            while candidate in reserved:
                candidate += "-ref"
            reserved.add(candidate)
            labels[label] = candidate
            hoist.add(label)
        if not hoist:
            result[origin] = originals[origin]
            continue
        body = []
        for text, visible in chunks:
            if not visible:
                body.append(text)
                continue
            masked, codes = _mask_reference_code(text)
            rewritten = []
            for line in masked.splitlines(keepends=True):
                match = REFERENCE_PATTERN.match(line)
                if match:
                    label = match[1].split("[", 1)[1].rsplit("]", 1)[0]
                    if normalize_spaces(label).casefold() in hoist:
                        continue
                    rewritten.append(line)
                else:
                    rewritten.append(_namespace_reference_uses(line, labels))
            body.append(_restore_reference_code("".join(rewritten), codes))
        # Hoist definitions so references survive even if their original section is skipped.
        hoisted = [f"[{labels.get(label, definitions[origin][label][0])}]: {definitions[origin][label][1]}"
                   for label in sorted(hoist)]
        result[origin] = ("".join(body).rstrip() + "\n\n## Retained Reference Definitions\n"
                          + "\n".join(hoisted) + "\n")
    return result


def _retain_source_sections(
    markdown: str, originals: dict[str, str],
    rebase_links: Callable[[str, str], str] | None = None,
) -> str:
    """Keep evidence/custom sections as attributed, non-nesting content blocks."""
    pipeline_sections = {"classification", "contributing courses", "extraction metadata",
                         "quality review", "retained source material"}
    current_sections = {name.lower(): content for name, content in _page_sections(markdown)}
    pattern = re.compile(r'<!-- retained-evidence (\{[^\n]+\}) -->\n(.*?)\n<!-- /retained-evidence -->', re.S)
    blocks: dict[tuple[str, str], dict] = {}

    def retain(section: str, content: str, sources: list[str]) -> None:
        content = content.strip("\n")
        if not content:
            return
        key = (section.lower(), sha256(content.encode()).hexdigest())
        block = blocks.setdefault(key, {"section": section, "content": content, "sources": set()})
        block["sources"].update(sources)

    for origin, original in sorted(_isolate_source_references(originals).items()):
        for match in pattern.finditer(original):
            header = json.loads(match[1])
            content = match[2].split("\n\n", 1)[1]
            if rebase_links:
                content = rebase_links(origin, content)
            retain(header["section"], content, header["sources"])
        # Retained blocks have their own stable attribution. Never nest them.
        cleaned = pattern.sub("", original)
        for section, content in _page_sections(cleaned):
            if section.lower() not in pipeline_sections and content != current_sections.get(section.lower()):
                if rebase_links:
                    content = rebase_links(origin, content)
                retain(section, content, [origin])
    if not blocks:
        return markdown
    rendered = ["## Retained Source Material"]
    for key, block in sorted(blocks.items()):
        header = {"section": block["section"], "digest": key[1], "sources": sorted(block["sources"])}
        rendered.extend(["", f"<!-- retained-evidence {json.dumps(header, ensure_ascii=True, sort_keys=True)} -->",
                         f"### {block['section']}", f"Source records: {', '.join(header['sources'])}", "",
                         block["content"], "<!-- /retained-evidence -->"])
    insertion = markdown.find("## Provenance")
    if insertion < 0:
        insertion = len(markdown)
    return markdown[:insertion].rstrip() + "\n\n" + "\n".join(rendered) + "\n\n" + markdown[insertion:]


def _rebase_evidence_links(content: str, source: Path, target: Path, archives: dict[Path, Path]) -> str:
    def rewrite(destination: str) -> str:
        url = urlsplit(destination)
        if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
            return destination
        original = (source / unquote(url.path)).resolve()
        mapped = original
        for directory, archive in sorted(archives.items(), key=lambda item: len(item[0].parts), reverse=True):
            if original.is_relative_to(directory):
                mapped = archive / original.relative_to(directory)
                break
        relative = os.path.relpath(mapped, target).replace(os.sep, "/")
        return urlunsplit(("", "", quote(relative, safe="/~"), url.query, url.fragment))
    parts = []
    for text, visible in _reference_text_parts(content):
        if not visible:
            parts.append(text)
            continue
        masked, codes = _mask_reference_code(text)
        parts.append(_restore_reference_code(map_document_links(masked, rewrite), codes))
    return "".join(parts)


def _metadata_from_page(record: ConceptRecord, concepts_root: Path) -> ConceptMetadata:
    """Retain literal page values when metadata omitted them, without synthesis."""
    path = record.directory / "concept.md"
    if not path.exists():
        return record.metadata
    names = {"definition": "definition", "core intuition": "intuition",
             "mathematical foundation": "mathematical_foundation"}
    values = {}
    conflicts = list(record.metadata.persistence_conflicts)
    for heading, content in _page_sections(path.read_text(encoding="utf-8")):
        field_name = names.get(heading.lower())
        if not field_name or not content:
            continue
        prior = getattr(record.metadata, field_name)
        if not prior:
            values[field_name] = content
        elif prior != content:
            conflicts.append(PersistenceConflict(field_name, prior, [PersistenceAlternative(
                record.directory.relative_to(concepts_root).as_posix(), sha256_file(record.metadata_path), content,
            )]))
    return replace(record.metadata, **values, persistence_conflicts=conflicts)


def _render_persistence_review(
    markdown: str, metadata: ConceptMetadata, history_prefix: str = "../../.concepts_history",
) -> str:
    if not metadata.persistence_conflicts:
        return markdown
    if "## Quality Review" not in markdown:
        markdown = markdown.rstrip() + "\n\n## Quality Review\n"
    lines = [markdown.rstrip(), "", "Unresolved persistence conflicts (preferred current values retained):"]
    for conflict in metadata.persistence_conflicts:
        for alternative in conflict.alternatives:
            if alternative.source_record.startswith("lecture:"):
                lines.append(f"- `{conflict.field_name}`: alternative from `{alternative.source_record}` "
                             f"(lecture SHA-256 `{alternative.record_sha256}`).")
                continue
            archive = f"{history_prefix}/{alternative.snapshot_id}/manifest.json"
            reference = f"[archive manifest]({archive})" if alternative.snapshot_id else "archive pending"
            lines.append(f"- `{conflict.field_name}`: alternative from `{alternative.source_record}` "
                         f"(metadata SHA-256 `{alternative.record_sha256}`; {reference}).")
    return "\n".join(lines) + "\n"


def consolidate_concepts(processed_root: Path, concepts_root: Path) -> ConsolidationReport:
    artifacts = discover_lecture_artifacts(processed_root)
    recover_concept_transactions(concepts_root)
    mentions_by_key, _lecture_hashes = collect_mentions(artifacts)
    grouped: dict[str, list[ConceptRecord]] = defaultdict(list)
    for record in discover_concept_records(concepts_root):
        grouped[record.key].append(record)
    report = ConsolidationReport(total_mentions=sum(len(v) for v in mentions_by_key.values()))
    for key in sorted(set(grouped) | set(mentions_by_key)):
        records = grouped.get(key, [])
        mentions = mentions_by_key.get(key, [])
        primary = _choose_primary_record(records) if records else None
        if len(records) == 1:
            hashes = {mention.lecture_file: mention.lecture_hash for mention in mentions}
            if all(primary.metadata.source_lecture_hashes.get(path) == digest for path, digest in hashes.items()):
                report.unchanged.append(key)
                continue
        existing = merge_concept_metadata(concepts_root, [
            (r.directory, _metadata_from_page(r, concepts_root)) for r in records
        ]) if records else None
        name = existing.concept_name if existing else _preferred_display_name(mentions, key)
        metadata = _merge_metadata(name, key, mentions, existing)
        directory = primary.directory if primary else concept_directory(concepts_root, name)
        originals = {}
        origin_directories = {}
        for record in records:
            path = record.directory / "concept.md"
            if path.exists():
                origin = record.directory.relative_to(concepts_root).as_posix()
                origin += f" (metadata SHA-256 {sha256_file(record.metadata_path)})"
                originals[origin] = path.read_text(encoding="utf-8")
                origin_directories[origin] = record.directory

        def render(final: ConceptMetadata) -> str:
            markdown = build_concept_markdown(name, key, final, mentions)
            snapshot = concept_history_root(concepts_root) / final.persistence_snapshot_id
            archives = {record.directory.resolve(): snapshot / "records" / f"{i:04d}"
                        for i, record in enumerate(sorted(records, key=lambda r: r.directory.as_posix()))}
            markdown = _retain_source_sections(markdown, originals, lambda origin, content: _rebase_evidence_links(
                content, origin_directories[origin], directory, archives,
            ))
            prefix = os.path.relpath(concept_history_root(concepts_root), directory).replace(os.sep, "/")
            return _render_persistence_review(markdown, final, prefix)

        superseded = tuple(r.directory for r in records if r != primary)
        result = write_concept_record(concepts_root, directory, metadata, render,
                                      superseded_directories=superseded,
                                      reason="duplicate merge" if superseded else "source update")
        if result.changed:
            (report.updated if primary else report.created).append(key)
            report.duplicate_dirs.extend(str(path) for path in superseded)
        else:
            report.unchanged.append(key)
    return report
