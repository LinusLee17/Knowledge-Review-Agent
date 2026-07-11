from __future__ import annotations

import json
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .concept_store import concept_paths, load_concept_metadata, save_concept_metadata
from .models import ConceptMetadata
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
    artifacts: list[LectureArtifact] = []
    for path in sorted(processed_root.rglob("lecture.json")):
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        artifacts.append(
            LectureArtifact(
                path=path,
                relative_path=path.relative_to(processed_root).as_posix(),
                sha256=sha256_file(path),
                payload=payload,
            )
        )
    return artifacts


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

    applications = _unique_text_list([*(item.get("applications", []) or []), *application_suffixes, *(profile.applications if profile else [])])
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
        mathematical_foundation=normalize_spaces(str(item.get("mathematical_foundation", "") or "")),
        assumptions=_unique_text_list(item.get("assumptions", []) or []),
        applications=applications,
        limitations=_unique_text_list(item.get("limitations", []) or []),
        advantages=_unique_text_list(item.get("advantages", []) or []),
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
                definition=heading,
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
    payload = artifact.payload
    course_id, course_name = _lecture_course(payload)
    mentions: list[ConceptMention] = []
    seen: set[tuple[str, int, str]] = set()

    for page in payload.get("pages", []) or []:
        page_number = int(page.get("page_number", 0) or 0)
        heading = normalize_spaces(str(page.get("heading", "") or ""))
        lines = normalize_lines(str(page.get("extracted_text", "") or ""))
        page_mentions: list[ConceptMention] = []
        structured = page.get("concepts", []) or []
        if structured:
            for item in structured:
                mention = _normalise_concept_source(item or {}, artifact, page_number, course_id, course_name)
                if mention:
                    page_mentions.append(mention)
        else:
            page_mentions = _fallback_mentions_from_candidates(
                artifact,
                page_number,
                heading,
                page.get("concept_candidates", []) or [],
                course_id,
                course_name,
            )

        for mention in page_mentions:
            evidence = normalize_spaces(mention.evidence or _select_evidence(mention.concept_label, heading, lines))
            dedupe_key = (mention.concept_key, page_number, evidence.lower())
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            mentions.append(
                ConceptMention(
                    concept_label=mention.concept_label,
                    concept_key=mention.concept_key,
                    concept_type=mention.concept_type,
                    domain=mention.domain,
                    topic=mention.topic,
                    importance_score=mention.importance_score,
                    confidence_score=mention.confidence_score,
                    evidence_strength=mention.evidence_strength,
                    definition_quality_score=mention.definition_quality_score,
                    interview_relevance=mention.interview_relevance,
                    reason_for_inclusion=mention.reason_for_inclusion,
                    definition=mention.definition,
                    intuition=mention.intuition,
                    mathematical_foundation=mention.mathematical_foundation,
                    assumptions=mention.assumptions,
                    applications=mention.applications,
                    limitations=mention.limitations,
                    advantages=mention.advantages,
                    broader_topics=mention.broader_topics,
                    prerequisites=mention.prerequisites,
                    related_concepts=mention.related_concepts,
                    aliases=mention.aliases,
                    course_id=mention.course_id,
                    course_name=mention.course_name,
                    lecture_file=mention.lecture_file,
                    lecture_hash=mention.lecture_hash,
                    source_pdf=mention.source_pdf,
                    page_number=mention.page_number,
                    page_heading=mention.page_heading,
                    evidence=evidence,
                )
            )

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


def _merge_existing_records(records: list[ConceptRecord]) -> ConceptRecord:
    primary = _choose_primary_record(records)
    merged_courses = sorted(
        set().union(*(record.metadata.contributing_courses for record in records))
    )
    merged_lecture_files = sorted(
        set().union(*(record.metadata.contributing_lecture_files for record in records))
    )
    merged_hashes: dict[str, str] = {}
    for record in records:
        merged_hashes.update(record.metadata.source_lecture_hashes or {})
    merged_related = sorted(set().union(*(record.metadata.related_concepts for record in records)))
    merged_prereqs = sorted(set().union(*(record.metadata.prerequisites for record in records)))
    merged_used_in = sorted(set().union(*(record.metadata.used_in for record in records)))
    merged_name = primary.metadata.concept_name or canonical_concept_name(primary.key) or primary.key
    merged_key = primary.metadata.canonical_key or primary.key
    merged_graph_node_id = primary.metadata.graph_node_id or slugify(primary.key)
    merged_timestamp = max(
        (record.metadata.last_updated_timestamp for record in records if record.metadata.last_updated_timestamp),
        default=primary.metadata.last_updated_timestamp,
    )

    merged_metadata = ConceptMetadata(
        concept_name=merged_name,
        canonical_key=merged_key,
        contributing_courses=merged_courses,
        contributing_lecture_files=merged_lecture_files,
        source_lecture_hashes=merged_hashes,
        last_updated_timestamp=merged_timestamp,
        version_number=max(record.metadata.version_number for record in records),
        related_concepts=merged_related,
        prerequisites=merged_prereqs,
        used_in=merged_used_in,
        graph_node_id=merged_graph_node_id,
    )

    if any(record.metadata != merged_metadata for record in records):
        merged_metadata = ConceptMetadata(
            concept_name=merged_metadata.concept_name,
            canonical_key=merged_metadata.canonical_key,
            contributing_courses=merged_metadata.contributing_courses,
            contributing_lecture_files=merged_metadata.contributing_lecture_files,
            source_lecture_hashes=merged_metadata.source_lecture_hashes,
            last_updated_timestamp=datetime.now(timezone.utc).isoformat(),
            version_number=max(record.metadata.version_number for record in records) + 1,
            related_concepts=merged_metadata.related_concepts,
            prerequisites=merged_metadata.prerequisites,
            used_in=merged_metadata.used_in,
            graph_node_id=merged_metadata.graph_node_id,
        )

    return ConceptRecord(
        key=primary.key,
        directory=primary.directory,
        metadata_path=primary.metadata_path,
        metadata=merged_metadata,
    )


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
    if summary:
        return summary

    profile = profile_for_label(concept_name)
    if profile:
        domain = metadata.domain or profile.domain
        topic = metadata.topic or profile.topic
        applications = ", ".join(metadata.applications[:3] or list(profile.applications)[:3]) if (metadata.applications or profile.applications) else ""
        parts = [f"{profile.concept_name} is a {profile.concept_type or 'concept'} in {domain or 'the target domain'}"]
        if topic:
            parts.append(f"focused on {topic}")
        base = " ".join(parts).strip() + "."
        if applications:
            base += f" It is used for {applications}."
        return base

    fallback = _merged_text_block(mentions, "definition")
    if fallback and normalize_concept_key(fallback) != normalize_concept_key(concept_name):
        return fallback
    return f"{concept_name} is a durable knowledge concept relevant to the course material."


def _synthesized_intuition(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    intuition = canonical_intuition_for_label(concept_name)
    if intuition:
        return intuition
    if metadata.intuition:
        return metadata.intuition
    fallback = _merged_text_block(mentions, "intuition")
    if fallback:
        return fallback
    return ""


def _synthesized_math(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    math = canonical_math_for_label(concept_name)
    if math:
        return math
    if metadata.mathematical_foundation:
        return metadata.mathematical_foundation
    fallback = _merged_text_block(mentions, "mathematical_foundation")
    return fallback


def _further_reading(concept_name: str) -> list[str]:
    return canonical_further_reading_for_label(concept_name)


def _why_it_matters(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    text = canonical_why_it_matters_for_label(concept_name)
    if text:
        return text
    applications = metadata.applications or _merged_text_list(mentions, "applications")
    related = metadata.related_concepts or _merged_text_list(mentions, "related_concepts")
    if applications:
        return (
            f"{concept_name} matters because it shows up in {', '.join(applications[:3])} "
            f"and gives you a reusable building block for the surrounding course material."
        )
    if related:
        return f"{concept_name} matters because it connects to {', '.join(related[:3])} and helps organize the topic."
    if metadata.domain or metadata.topic:
        return f"{concept_name} matters because it is a durable concept in {metadata.domain or 'the target domain'}."
    return ""


def _how_it_works(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> str:
    text = canonical_how_it_works_for_label(concept_name)
    if text:
        return text
    definition = _synthesized_definition(concept_name, metadata, mentions)
    intuition = _synthesized_intuition(concept_name, metadata, mentions)
    pieces = [piece for piece in (definition, intuition) if piece]
    if pieces:
        return "\n\n".join(pieces)
    return ""


def _key_components(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    components = canonical_key_components_for_label(concept_name)
    if components:
        return components
    components = metadata.prerequisites or _merged_text_list(mentions, "prerequisites")
    if components:
        return components[:5]
    return []


def _common_variants(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    variants = canonical_common_variants_for_label(concept_name)
    if variants:
        return variants
    aliases = metadata.aliases or _merged_text_list(mentions, "aliases")
    if aliases:
        return [alias for alias in aliases if normalize_concept_key(alias) != normalize_concept_key(concept_name)][:5]
    return []


def _common_mistakes(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    mistakes = canonical_common_mistakes_for_label(concept_name)
    if mistakes:
        return mistakes
    items: list[str] = []
    if metadata.limitations:
        items.extend(metadata.limitations[:3])
    if not items:
        items.append(f"Do not memorize {concept_name} without understanding its role in the surrounding topic.")
    return _unique_text_list(items)


def _interview_questions(concept_name: str, metadata: ConceptMetadata, mentions: list[ConceptMention]) -> list[str]:
    questions = canonical_interview_questions_for_label(concept_name)
    if questions:
        return questions
    fallback = [
        f"What problem does {concept_name} solve?",
        f"How does {concept_name} work at a high level?",
        f"When would you use {concept_name}, and when would you avoid it?",
        f"What are the main assumptions or limitations of {concept_name}?",
    ]
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
    definition = _synthesized_definition(concept_name, metadata, mentions)
    why_it_matters = _why_it_matters(concept_name, metadata, mentions)
    intuition = _synthesized_intuition(concept_name, metadata, mentions)
    how_it_works = _how_it_works(concept_name, metadata, mentions)
    mathematical_foundation = _synthesized_math(concept_name, metadata, mentions)
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

    lines = [
        "---",
        f'concept_name: "{concept_name}"',
        f'canonical_key: "{canonical_key}"',
        f'concept_type: "{getattr(metadata, "concept_type", "")}"',
        f'domain: "{metadata.domain}"',
        f'topic: "{metadata.topic}"',
        f"importance_score: {metadata.importance_score}",
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
        f"- importance: {metadata.importance_score}/5",
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
        return _unique_text_list(values)

    if existing:
        merged_courses = sorted(set(existing.contributing_courses + course_names))
        merged_lecture_files = sorted(set(existing.contributing_lecture_files + lecture_files))
        merged_hashes = dict(existing.source_lecture_hashes)
        merged_hashes.update(lecture_hashes)
        merged_related = _merged_list("related_concepts")
        merged_prereqs = _merged_list("prerequisites")
        merged_used_in = _merged_list("used_in")
        merged_assumptions = _merged_list("assumptions")
        merged_applications = _merged_list("applications")
        merged_limitations = _merged_list("limitations")
        merged_advantages = _merged_list("advantages")
        merged_broader_topics = _merged_list("broader_topics")
        merged_aliases = _merged_list("aliases")
        merged_domain = _best_text("domain", existing.domain)
        merged_topic = _best_text("topic", existing.topic)
        merged_definition = _best_text("definition", existing.definition)
        merged_intuition = _best_text("intuition", existing.intuition)
        merged_math = _best_text("mathematical_foundation", existing.mathematical_foundation)
        merged_concept_type = _best_text("concept_type", getattr(existing, "concept_type", ""))
        merged_confidence_score = max([getattr(existing, "confidence_score", 0.0), *[getattr(mention, "confidence_score", 0.0) for mention in mentions]], default=getattr(existing, "confidence_score", 0.0))
        merged_evidence_strength = max([getattr(existing, "evidence_strength", 0.0), *[getattr(mention, "evidence_strength", 0.0) for mention in mentions]], default=getattr(existing, "evidence_strength", 0.0))
        merged_definition_quality_score = max([getattr(existing, "definition_quality_score", 0.0), *[getattr(mention, "definition_quality_score", 0.0) for mention in mentions]], default=getattr(existing, "definition_quality_score", 0.0))
        merged_interview_relevance = max([getattr(existing, "interview_relevance", 0.0), *[getattr(mention, "interview_relevance", 0.0) for mention in mentions]], default=getattr(existing, "interview_relevance", 0.0))
        merged_importance = max([existing.importance_score, *[mention.importance_score for mention in mentions]])
        merged_graph_node_id = existing.graph_node_id or slugify(canonical_key)
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
            contributing_courses=merged_courses,
            contributing_lecture_files=merged_lecture_files,
            source_lecture_hashes=merged_hashes,
            last_updated_timestamp=now,
            version_number=existing.version_number + 1,
            related_concepts=merged_related,
            prerequisites=merged_prereqs,
            used_in=merged_used_in,
            graph_node_id=merged_graph_node_id,
        )
        merged_definition = _synthesized_definition(concept_name, preview_metadata, mentions)
        merged_intuition = _synthesized_intuition(concept_name, preview_metadata, mentions)
        merged_math = _synthesized_math(concept_name, preview_metadata, mentions)
        changed = (
            existing.concept_name != concept_name
            or existing.canonical_key != canonical_key
            or getattr(existing, "concept_type", "") != merged_concept_type
            or existing.domain != merged_domain
            or existing.topic != merged_topic
            or existing.importance_score != merged_importance
            or existing.definition != merged_definition
            or existing.intuition != merged_intuition
            or existing.mathematical_foundation != merged_math
            or existing.assumptions != merged_assumptions
            or existing.applications != merged_applications
            or existing.limitations != merged_limitations
            or existing.advantages != merged_advantages
            or existing.broader_topics != merged_broader_topics
            or existing.aliases != merged_aliases
            or existing.contributing_courses != merged_courses
            or existing.contributing_lecture_files != merged_lecture_files
            or existing.source_lecture_hashes != merged_hashes
            or existing.related_concepts != merged_related
            or existing.prerequisites != merged_prereqs
            or existing.used_in != merged_used_in
        )

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
            contributing_courses=merged_courses,
            contributing_lecture_files=merged_lecture_files,
            source_lecture_hashes=merged_hashes,
            last_updated_timestamp=now if changed else existing.last_updated_timestamp,
            version_number=existing.version_number + 1 if changed else existing.version_number,
            related_concepts=merged_related,
            prerequisites=merged_prereqs,
            used_in=merged_used_in,
            graph_node_id=merged_graph_node_id,
        )

    merged_assumptions = _merged_list("assumptions")
    merged_applications = _merged_list("applications")
    merged_limitations = _merged_list("limitations")
    merged_advantages = _merged_list("advantages")
    merged_broader_topics = _merged_list("broader_topics")
    merged_aliases = _merged_list("aliases")
    merged_related = _merged_list("related_concepts")
    merged_prereqs = _merged_list("prerequisites")
    merged_used_in = _merged_list("used_in")
    merged_domain = _best_text("domain")
    merged_topic = _best_text("topic")
    merged_definition = _best_text("definition")
    merged_intuition = _best_text("intuition")
    merged_math = _best_text("mathematical_foundation")
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


def _write_concept_record(
    directory: Path,
    metadata_path: Path,
    concept_name: str,
    canonical_key: str,
    metadata: ConceptMetadata,
    mentions: list[ConceptMention],
    *,
    force: bool = False,
) -> bool:
    directory.mkdir(parents=True, exist_ok=True)
    concept_md_path = directory / "concept.md"
    markdown = build_concept_markdown(concept_name, canonical_key, metadata, mentions)
    existing_markdown = concept_md_path.read_text(encoding="utf-8") if concept_md_path.exists() else None
    existing_metadata = load_concept_metadata(metadata_path)

    if not force and existing_markdown == markdown and existing_metadata == metadata:
        return False

    concept_md_path.write_text(markdown, encoding="utf-8")
    save_concept_metadata(metadata_path, metadata)
    return True


def consolidate_concepts(processed_root: Path, concepts_root: Path) -> ConsolidationReport:
    artifacts = discover_lecture_artifacts(processed_root)
    mentions_by_key, _lecture_hashes = collect_mentions(artifacts)
    existing_records = discover_concept_records(concepts_root)

    records_by_key: dict[str, list[ConceptRecord]] = defaultdict(list)
    for record in existing_records:
        records_by_key[record.key].append(record)

    report = ConsolidationReport(total_mentions=sum(len(v) for v in mentions_by_key.values()))

    for key, records in sorted(list(records_by_key.items())):
        if len(records) <= 1:
            continue
        primary_record = _choose_primary_record(records)
        merged_record = _merge_existing_records(records)
        records_by_key[key] = [merged_record]
        for duplicate in records:
            if duplicate.directory == primary_record.directory:
                continue
            report.duplicate_dirs.append(duplicate.directory.as_posix())
            if duplicate.directory.exists():
                shutil.rmtree(duplicate.directory)
        concept_name = merged_record.metadata.concept_name or _preferred_display_name(mentions_by_key.get(key, []), key)
        if _write_concept_record(
            primary_record.directory,
            primary_record.metadata_path,
            concept_name,
            key,
            merged_record.metadata,
            [],
            force=True,
        ):
            report.updated.append(key)

    current_keys = set(mentions_by_key.keys())
    for key in sorted(current_keys):
        mentions = mentions_by_key[key]
        existing_record = records_by_key.get(key, [None])[0] if records_by_key.get(key) else None
        existing_meta = existing_record.metadata if existing_record else None
        concept_name = (
            existing_meta.concept_name
            if existing_meta and existing_meta.concept_name
            else _preferred_display_name(mentions, key)
        )
        current_meta = _merge_metadata(concept_name, key, mentions, existing_meta)

        if existing_record:
            directory = existing_record.directory
            metadata_path = existing_record.metadata_path
        else:
            directory = concepts_root / concept_name
            metadata_path = concept_paths(concepts_root, concept_name)[1]

        if _write_concept_record(
            directory,
            metadata_path,
            concept_name,
            key,
            current_meta,
            mentions,
        ):
            if existing_meta:
                if key not in report.updated:
                    report.updated.append(key)
            else:
                report.created.append(key)
        else:
            report.unchanged.append(key)

    return report
