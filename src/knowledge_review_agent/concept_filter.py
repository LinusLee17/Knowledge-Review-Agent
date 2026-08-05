from __future__ import annotations

import json
import re
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .metadata import load_metadata, resolve_course
from .concept_rules import (
    CONCEPT_CONFIDENCE_THRESHOLD,
    DEFINITION_QUALITY_THRESHOLD,
    EVIDENCE_STRENGTH_THRESHOLD,
    INTERVIEW_RELEVANCE_THRESHOLD,
    candidate_concepts_from_page,
    domain_family,
    educational_importance_prior,
    graph_support_prior,
    profile_for_label,
    same_domain_family,
)
from .models import (
    ConceptCandidate,
    ConceptExtraction,
    CourseMetadata,
    DocumentExtraction,
    ExtractionMetrics,
    PageExtraction,
    RejectedConcept,
)
from .pdf_skill_adapter import (
    ExternalPdfSkillBridge,
    PdfSkillBridge,
    PARSER_VERSION,
    result_to_document_extraction,
)
from .utils import (
    markdown_escape_cell,
    normalize_concept,
    normalize_concept_key,
    normalize_lines,
    normalize_spaces,
)


# These topics are often taught across many sparse slides: the slide has strong
# topic evidence, while definition/math/application fields are distributed over
# the lecture. Accept only when both confidence and evidence are substantial.
CURATED_FOUNDATION_CONCEPTS = {
    "bayesian network",
    "markov model",
    "hidden markov model",
    "reinforcement learning",
    "sampling",
    "causal inference",
    "experiment design",
    "internal validity",
    "model selection",
    "dimensionality reduction",
}


def discover_pdfs(raw_root: Path) -> list[Path]:
    return sorted(
        path
        for path in raw_root.rglob("*.pdf")
        if path.is_file() and not path.name.startswith(".")
    )


def _default_graph_json() -> Path:
    return Path(__file__).resolve().parents[2] / "knowledge_base" / "graphs" / "graph.json"


def load_graph_context(graph_json_path: Path | None = None) -> dict[str, int]:
    path = graph_json_path or _default_graph_json()
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    context: dict[str, int] = {}
    for node in payload.get("nodes", []) or []:
        key = normalize_concept_key(str(node.get("concept_key") or node.get("concept_name") or ""))
        if not key:
            continue
        context[key] = int(node.get("degree", node.get("connected_edge_count", 0)) or 0)
    return context


def _course_domain(course: CourseMetadata) -> str:
    course_id = (course.course_id or "").upper()
    if course_id.startswith("ST"):
        return "Statistics"
    if course_id.startswith(("CS", "BT42")):
        return "Machine Learning"
    if course_id.startswith(("BT4012", "BT2102")):
        return "Data Science"
    if course_id.startswith("IS"):
        course_name = (course.course_name or "").lower()
        if "leadership" in course_name or "communication" in course_name:
            return "Leadership"
        return "Leadership"
    return course.category or ""


def table_to_markdown(table: list[list[str]]) -> str:
    if not table:
        return ""

    rows = [[markdown_escape_cell(cell or "") for cell in row] for row in table]
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]

    header = rows[0]
    lines = ["| " + " | ".join(header) + " |"]
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _normalize_text_line(line: str) -> str:
    stripped = normalize_concept(line)
    stripped = re.sub(r"^[-*•]\s*", "", stripped)
    stripped = re.sub(r"^[0-9]+[.)]\s*", "", stripped)
    return normalize_concept(stripped)


def _text_contains_term(text: str, term: str) -> bool:
    text = normalize_concept(text).lower()
    term = normalize_concept(term).lower()
    if not text or not term:
        return False
    if len(term) <= 3 or len(term.split()) == 1:
        return re.search(rf"(?<![a-z0-9]){re.escape(term)}(?![a-z0-9])", text) is not None
    return term in text


def _term_hits_line(line: str, terms: list[str]) -> bool:
    return any(_text_contains_term(line, term) for term in terms)


def _relevant_lines(lines: list[str], terms: list[str], limit: int = 4) -> list[str]:
    results: list[str] = []
    for line in lines:
        if _term_hits_line(line, terms):
            cleaned = _normalize_text_line(line)
            if cleaned and cleaned not in results:
                results.append(cleaned)
        if len(results) >= limit:
            break
    return results


def _extract_definition(candidate: ConceptCandidate, lines: list[str], heading: str) -> str:
    terms = [candidate.concept_name, *candidate.aliases]
    cues = (
        " is ",
        " are ",
        ": a ",
        " shared collection ",
        " integrated collection ",
        " consists of ",
        " comprises ",
        " designed to ",
        " used to ",
        " refers to ",
        " means ",
        " defined as ",
        " model that ",
        " method that ",
        " approach that ",
        " framework that ",
        " strategy that ",
        " practice that ",
        " skill that ",
        " process that ",
        " principle that ",
        " estimates ",
        " measures ",
        " predicts ",
        " describes ",
        " leadership",
        " communication",
        " stakeholder",
        " transformation",
    )
    for line in [heading, *lines]:
        lower = line.lower()
        if _term_hits_line(line, terms) and any(cue in lower for cue in cues):
            cleaned = _normalize_text_line(line)
            if cleaned:
                return cleaned
    # PDF extraction often splits a definition over adjacent lines. Rejoin the
    # page before giving up, then keep only the sentence carrying the concept.
    joined = normalize_spaces(" ".join(lines))
    if joined and _term_hits_line(joined, terms) and any(cue in joined.lower() for cue in cues):
        for sentence in re.split(r"(?<=[.!?])\s+", joined):
            if _term_hits_line(sentence, terms) and len(sentence.split()) >= 8:
                return _normalize_text_line(sentence)[:500]
        return _normalize_text_line(joined)[:500]
    for line in lines:
        lower = line.lower()
        if _term_hits_line(line, terms) and len(line.split()) <= 40 and any(
            word in lower
            for word in (
                "prediction",
                "estimation",
                "classification",
                "optimization",
                "regression",
                "detection",
                "testing",
                "reduction",
                "probability",
                "relationship",
                "model",
                "method",
                "algorithm",
                "metric",
                "leadership",
                "communication",
                "stakeholder",
                "change",
                "strategy",
                "culture",
                "collaboration",
        "transformation",
        " stores ",
        " retrieves ",
        " queries ",
        " visualizes ",
        " communicates ",
        "stores",
        "retrieves",
        "queries",
        "visualizes",
        "communicates",
                "project",
                "business",
            )
        ):
            cleaned = _normalize_text_line(line)
            if cleaned:
                return cleaned
    return ""


def _extract_math(candidate: ConceptCandidate, lines: list[str]) -> str:
    if domain_family(candidate.domain) == "professional":
        return ""
    if candidate.importance_score < 5:
        return ""
    terms = [candidate.concept_name, *candidate.aliases]
    results: list[str] = []
    for line in lines:
        lower = line.lower()
        if not _term_hits_line(line, terms):
            continue
        if any(token in lower for token in ("=", "minimize", "maximize", "argmin", "argmax", "beta", "theta", "variance", "loss", "gradient", "likelihood", "log")):
            cleaned = _normalize_text_line(line)
            if cleaned and len(cleaned.split()) > 3 and cleaned not in results:
                results.append(cleaned)
        if len(results) >= 2:
            break
    return " ".join(results)


def _extract_applications(candidate: ConceptCandidate, lines: list[str]) -> list[str]:
    terms = [candidate.concept_name, *candidate.aliases]
    results: list[str] = []
    for line in lines:
        lower = line.lower()
        if not _term_hits_line(line, terms):
            continue
        if any(cue in lower for cue in ("used for", "applied to", "application", "predict", "classify", "forecast", "segment", "estimate", "detect", "diagnose")):
            cleaned = _normalize_text_line(line)
            if cleaned and cleaned not in results:
                results.append(cleaned)
        if len(results) >= 4:
            break
    return results


def _extract_field_lines(candidate: ConceptCandidate, lines: list[str], cue_words: tuple[str, ...], limit: int = 3) -> list[str]:
    terms = [candidate.concept_name, *candidate.aliases]
    results: list[str] = []
    for line in lines:
        lower = line.lower()
        if not _term_hits_line(line, terms):
            continue
        if any(cue in lower for cue in cue_words):
            cleaned = _normalize_text_line(line)
            if cleaned and cleaned not in results:
                results.append(cleaned)
        if len(results) >= limit:
            break
    return results


_GENERIC_PROSE_PHRASES = (
    "durable idea worth remembering because it appears repeatedly in the course material",
    "durable concept worth remembering because it appears repeatedly in the course material",
    "durable knowledge concept relevant to the course material",
    "think of",
    "repeatable procedure",
    "core rule or update procedure",
    "the mathematical form follows the update rule, objective function, or optimization criterion used by the method",
)

_SUBSTANTIVE_VERBS = (
    "estimates",
    "based",
        "designed",
        "describes",
        "organizes",
        "stores",
        "supports",
        "represents",
        "defines",
        "ensures",
        "retrieves",
        "queries",
        "joins",
        "visualizes",
        "communicates",
    "maps",
    "predicts",
    "measures",
    "updates",
    "minimizes",
    "maximizes",
    "splits",
    "projects",
    "computes",
    "fits",
    "optimizes",
    "compares",
    "thresholds",
    "reduces",
    "selects",
    "classifies",
)


def _is_substantive_text(text: str, concept_name: str) -> bool:
    cleaned = normalize_spaces(text)
    if not cleaned:
        return False
    lower = cleaned.lower()
    if normalize_concept_key(cleaned) == normalize_concept_key(concept_name):
        return False
    if len(cleaned.split()) < 8:
        return False
    if any(phrase in lower for phrase in _GENERIC_PROSE_PHRASES):
        return False
    if concept_name.lower() in lower and not any(verb in lower for verb in _SUBSTANTIVE_VERBS):
        return False
    return True


def _extraction_depth_score(concept: ConceptExtraction) -> float:
    if domain_family(concept.domain) == "professional":
        score = 0.0
        if _is_substantive_text(concept.definition, concept.concept_name):
            score += 0.42
        if _is_substantive_text(concept.intuition, concept.concept_name):
            score += 0.20
        if concept.applications:
            score += 0.10
        if concept.limitations:
            score += 0.05
        if concept.advantages:
            score += 0.05
        if concept.assumptions:
            score += 0.03
        if concept.prerequisites:
            score += 0.05
        if concept.related_concepts:
            score += 0.05
        if concept.broader_topics:
            score += 0.04
        if _is_substantive_text(concept.definition, concept.concept_name) and (
            concept.applications or concept.related_concepts or concept.prerequisites
        ):
            score += 0.06
        return min(1.0, score)

    score = 0.0
    if _is_substantive_text(concept.definition, concept.concept_name):
        score += 0.35
    if _is_substantive_text(concept.intuition, concept.concept_name):
        score += 0.15
    if _is_substantive_text(concept.mathematical_foundation, concept.concept_name):
        score += 0.20
    if concept.assumptions:
        score += 0.04
    if concept.applications:
        score += 0.06
    if concept.limitations:
        score += 0.04
    if concept.advantages:
        score += 0.04
    if concept.prerequisites:
        score += 0.04
    if concept.related_concepts:
        score += 0.04
    if concept.broader_topics:
        score += 0.04
    if _is_substantive_text(concept.definition, concept.concept_name) and (
        _is_substantive_text(concept.intuition, concept.concept_name)
        or _is_substantive_text(concept.mathematical_foundation, concept.concept_name)
    ):
        score += 0.08
    return min(1.0, score)


def _build_concept_extraction(
    candidate: ConceptCandidate,
    lines: list[str],
    heading: str,
    course: CourseMetadata,
    page_number: int,
    source_pdf: str,
) -> ConceptExtraction:
    canonical_name = candidate.concept_name
    profile = profile_for_label(canonical_name)
    aliases = list(dict.fromkeys([canonical_name, *candidate.aliases]))
    definition = _extract_definition(candidate, lines, heading)
    intuition = _extract_field_lines(candidate, lines, ("intuition", "intuitively", "idea", "goal", "aim", "helps", "captures", "in practice"), limit=2)
    mathematical_foundation = _extract_math(candidate, lines)
    assumptions = _extract_field_lines(candidate, lines, ("assumption", "assumes", "requires", "under the assumption", "conditions"), limit=3)
    applications = list(profile.applications) if profile else _extract_applications(candidate, lines)
    limitations = _extract_field_lines(candidate, lines, ("limitation", "limitations", "drawback", "fails", "cannot", "not suitable", "sensitive"), limit=3)
    advantages = _extract_field_lines(candidate, lines, ("advantage", "advantages", "benefit", "benefits", "strength", "interpretable", "efficient", "robust"), limit=3)
    prerequisites = list(profile.prerequisites) if profile else []
    related = list(profile.related_concepts) if profile else []
    broader_topics = list(profile.broader_topics) if profile else []
    if candidate.domain and candidate.domain not in broader_topics:
        broader_topics.append(candidate.domain)
    if candidate.topic and candidate.topic not in broader_topics:
        broader_topics.append(candidate.topic)

    return ConceptExtraction(
        concept_name=canonical_name,
        concept_type=candidate.concept_type or (profile.concept_type if profile else ""),
        domain=candidate.domain,
        topic=candidate.topic,
        importance_score=candidate.importance_score,
        scope_level=candidate.scope_level,
        study_priority=candidate.study_priority,
        confidence_score=candidate.confidence_score,
        confidence_reason=candidate.reason_for_inclusion,
        evidence_strength=candidate.evidence_strength,
        definition_quality_score=candidate.definition_quality_score,
        interview_relevance=candidate.interview_relevance,
        reason_for_inclusion=candidate.reason_for_inclusion,
        definition=definition,
        intuition=" ".join(intuition),
        mathematical_foundation=mathematical_foundation,
        assumptions=assumptions,
        applications=applications,
        limitations=limitations,
        advantages=advantages,
        prerequisites=prerequisites,
        related_concepts=related,
        broader_topics=broader_topics,
        aliases=aliases,
        canonical_key=normalize_concept_key(canonical_name),
        evidence=candidate.evidence,
        source={
            "course": course.course_id or course.course_name,
            "lecture": course.course_name or course.course_id,
            "page": str(page_number),
            "pdf": source_pdf,
        },
    )


def build_structured_concepts(
    text_lines: list[str],
    heading: str,
    tables: list[list[list[str]]],
    course: CourseMetadata,
    page_number: int,
    source_pdf: str,
    lecture_context: str = "",
    lecture_lines: list[str] | None = None,
    graph_context: dict[str, int] | None = None,
) -> tuple[list[ConceptCandidate], list[ConceptExtraction], list[RejectedConcept], dict[str, int]]:
    course_domain = _course_domain(course)
    course_family = domain_family(course_domain)
    candidate_details = candidate_concepts_from_page(
        heading,
        text_lines,
        tables,
        course.course_name,
        lecture_context=lecture_context,
        lecture_lines=lecture_lines,
        graph_context=graph_context,
    )
    approved: list[ConceptExtraction] = []
    rejected: list[RejectedConcept] = []
    metrics = {
        "candidate_concepts_generated": len(candidate_details),
        "concepts_accepted": 0,
        "concepts_rejected": 0,
        "rejected_low_confidence": 0,
        "rejected_structural_noise": 0,
        "rejected_ocr_noise": 0,
        "rejected_generic_term": 0,
        "rejected_weak_definition": 0,
        "rejected_low_depth": 0,
    }

    support_lines = [*text_lines, *(lecture_lines or [])]
    seen: set[str] = set()
    for candidate in candidate_details:
        importance_prior = educational_importance_prior(candidate.concept_name, lecture_context, course.course_name)
        graph_prior = graph_support_prior(candidate.concept_name, graph_context)
        lecture_support = min(1.0, sum(1 for line in support_lines if candidate.concept_name.lower() in line.lower()) / 4.0)
        candidate_domain = candidate.domain or (profile_for_label(candidate.concept_name).domain if profile_for_label(candidate.concept_name) else "")
        candidate_family = domain_family(candidate_domain)
        domain_match = (
            not course_domain
            or not candidate_domain
            or candidate_domain == course_domain
            or same_domain_family(candidate_domain, course_domain)
        )
        professional_family = course_family == "professional" or candidate_family == "professional"
        confidence_threshold = 0.46 if professional_family else CONCEPT_CONFIDENCE_THRESHOLD
        evidence_threshold = 0.24 if professional_family else EVIDENCE_STRENGTH_THRESHOLD
        definition_threshold = 0.22 if professional_family else DEFINITION_QUALITY_THRESHOLD
        relevance_threshold = 0.33 if professional_family else INTERVIEW_RELEVANCE_THRESHOLD
        importance_threshold = 0.72 if professional_family else 0.92
        depth_threshold = 0.32 if professional_family else 0.55
        # Data-management foundations often have strong source definitions but
        # little mathematics. Accept them when evidence and importance are high.
        if (
            candidate.domain == "Data Science"
            and candidate.importance_score >= 4
            and candidate.evidence_strength >= 0.68
            and candidate.definition_quality_score >= 0.58
        ):
            depth_threshold = 0.45
        selection_score = candidate.confidence_score
        selection_score += 0.12 * importance_prior
        selection_score += 0.06 * graph_prior
        selection_score += 0.04 * lecture_support
        importance_eligible = (
            importance_prior >= importance_threshold
            and domain_match
            and candidate.evidence_strength >= evidence_threshold
            and (candidate.definition_quality_score >= definition_threshold or lecture_support >= 0.5)
        )
        profile = profile_for_label(candidate.concept_name)
        curated_foundation_override = (
            normalize_concept_key(candidate.concept_name) in CURATED_FOUNDATION_CONCEPTS
            and candidate.confidence_score >= 0.55
            and candidate.evidence_strength >= 0.58
        )
        auto_ml_seed = (
            profile is not None
            and profile.topic == "AutoML"
            and profile.importance_score >= 4
            and candidate.confidence_score >= 0.40
            and candidate.evidence_strength >= 0.34
        )
        auto_ml_heading_seed = (
            profile is not None
            and profile.topic == "AutoML"
            and profile.importance_score >= 5
            and candidate.evidence_strength >= 0.30
            and any(alias.lower() in heading.lower() for alias in (profile.concept_name, *profile.synonyms))
        )
        auto_ml_acceptance_override = auto_ml_seed or auto_ml_heading_seed

        if candidate.concept_name.lower() in {"agenda", "introduction", "summary"}:
            metrics["concepts_rejected"] += 1
            metrics["rejected_structural_noise"] += 1
            rejected.append(
                RejectedConcept(
                    concept_name=candidate.concept_name,
                    reason="structural noise",
                    concept_type=candidate.concept_type,
                    confidence_score=candidate.confidence_score,
                    evidence_strength=candidate.evidence_strength,
                    definition_quality_score=candidate.definition_quality_score,
                    interview_relevance=candidate.interview_relevance,
                    domain=candidate.domain,
                    topic=candidate.topic,
                    evidence=candidate.evidence,
                )
            )
            continue
        if candidate.confidence_score < confidence_threshold and selection_score < confidence_threshold and not importance_eligible and not auto_ml_acceptance_override and not curated_foundation_override:
            metrics["concepts_rejected"] += 1
            metrics["rejected_low_confidence"] += 1
            rejected.append(
                RejectedConcept(
                    concept_name=candidate.concept_name,
                    reason="low confidence",
                    concept_type=candidate.concept_type,
                    confidence_score=candidate.confidence_score,
                    evidence_strength=candidate.evidence_strength,
                    definition_quality_score=candidate.definition_quality_score,
                    interview_relevance=candidate.interview_relevance,
                    domain=candidate.domain,
                    topic=candidate.topic,
                    evidence=candidate.evidence,
                )
            )
            continue
        if candidate.evidence_strength < evidence_threshold and not importance_eligible and not auto_ml_acceptance_override and not curated_foundation_override:
            metrics["concepts_rejected"] += 1
            metrics["rejected_low_confidence"] += 1
            rejected.append(
                RejectedConcept(
                    concept_name=candidate.concept_name,
                    reason="insufficient evidence",
                    concept_type=candidate.concept_type,
                    confidence_score=candidate.confidence_score,
                    evidence_strength=candidate.evidence_strength,
                    definition_quality_score=candidate.definition_quality_score,
                    interview_relevance=candidate.interview_relevance,
                    domain=candidate.domain,
                    topic=candidate.topic,
                    evidence=candidate.evidence,
                )
            )
            continue
        if candidate.definition_quality_score < definition_threshold and not importance_eligible and not auto_ml_acceptance_override and not curated_foundation_override:
            metrics["concepts_rejected"] += 1
            metrics["rejected_weak_definition"] += 1
            if candidate.concept_name.lower() in {"accuracy", "prediction", "model", "training", "feature", "data", "classification", "regression"}:
                metrics["rejected_generic_term"] += 1
            rejected.append(
                RejectedConcept(
                    concept_name=candidate.concept_name,
                    reason="weak definition",
                    concept_type=candidate.concept_type,
                    confidence_score=candidate.confidence_score,
                    evidence_strength=candidate.evidence_strength,
                    definition_quality_score=candidate.definition_quality_score,
                    interview_relevance=candidate.interview_relevance,
                    domain=candidate.domain,
                    topic=candidate.topic,
                    evidence=candidate.evidence,
                )
            )
            continue
        if candidate.interview_relevance < relevance_threshold and not importance_eligible and not auto_ml_acceptance_override and not curated_foundation_override:
            metrics["concepts_rejected"] += 1
            metrics["rejected_low_depth"] += 1
            rejected.append(
                RejectedConcept(
                    concept_name=candidate.concept_name,
                    reason="low interview relevance",
                    concept_type=candidate.concept_type,
                    confidence_score=candidate.confidence_score,
                    evidence_strength=candidate.evidence_strength,
                    definition_quality_score=candidate.definition_quality_score,
                    interview_relevance=candidate.interview_relevance,
                    domain=candidate.domain,
                    topic=candidate.topic,
                    evidence=candidate.evidence,
                )
            )
            continue
        key = normalize_concept_key(candidate.concept_name)
        if not key or key in seen:
            metrics["concepts_rejected"] += 1
            metrics["rejected_low_confidence"] += 1
            rejected.append(
                RejectedConcept(
                    concept_name=candidate.concept_name,
                    reason="duplicate or unresolved concept key",
                    concept_type=candidate.concept_type,
                    confidence_score=candidate.confidence_score,
                    evidence_strength=candidate.evidence_strength,
                    definition_quality_score=candidate.definition_quality_score,
                    interview_relevance=candidate.interview_relevance,
                    domain=candidate.domain,
                    topic=candidate.topic,
                    evidence=candidate.evidence,
                )
            )
            continue
        extraction = _build_concept_extraction(candidate, text_lines, heading, course, page_number, source_pdf)
        depth_score = _extraction_depth_score(extraction)
        # AutoML slides often define a method and compare it across several
        # pages, without repeating intuition/math/application fields on each
        # page. Strong source evidence + a usable definition is enough for a
        # seeded AutoML profile; ordinary concepts keep the normal depth gate.
        if (auto_ml_acceptance_override or curated_foundation_override) and depth_score < depth_threshold:
            depth_score = depth_threshold
        # Educational importance may rescue weak confidence, but never an explanation
        # that lacks enough substance to justify a standalone knowledge page.
        if depth_score < depth_threshold:
            metrics["concepts_rejected"] += 1
            metrics["rejected_low_depth"] += 1
            rejected.append(
                RejectedConcept(
                    concept_name=candidate.concept_name,
                    reason="low extracted depth",
                    concept_type=candidate.concept_type,
                    confidence_score=candidate.confidence_score,
                    evidence_strength=candidate.evidence_strength,
                    definition_quality_score=candidate.definition_quality_score,
                    interview_relevance=candidate.interview_relevance,
                    domain=candidate.domain,
                    topic=candidate.topic,
                    evidence=candidate.evidence,
                )
            )
            continue
        seen.add(key)
        approved.append(extraction)
        metrics["concepts_accepted"] += 1

    return candidate_details, approved, rejected, metrics


def build_page_markdown(
    relative_pdf: Path,
    course: CourseMetadata,
    page: PageExtraction,
) -> str:
    lines = [
        "---",
        f'source_pdf: "{relative_pdf.as_posix()}"',
        f"source_page: {page.page_number}",
        f'course_id: "{course.course_id}"',
        f'course_name: "{course.course_name}"',
        f'category: "{course.category}"',
        f'semester: "{course.semester}"',
        f'title: "{page.heading}"',
        f'extracted_at: "{datetime.now(timezone.utc).isoformat()}"',
        "---",
        "",
        f"# Page {page.page_number}" + (f": {page.heading}" if page.heading else ""),
        "",
        f"- source: `{relative_pdf.as_posix()}`",
        f"- page: `{page.page_number}`",
        f"- course_id: `{course.course_id}`",
        f"- course_name: `{course.course_name}`",
    ]

    if page.heading:
        lines.extend(["", "## Heading", "", page.heading])

    if page.extracted_text.strip():
        lines.extend(["", "## Extracted text", "", "```text", page.extracted_text.strip(), "```"])

    if page.tables:
        lines.extend(["", "## Tables"])
        for index, table in enumerate(page.tables, start=1):
            table_md = table_to_markdown(table)
            if not table_md:
                continue
            lines.extend(["", f"### Table {index}", "", table_md])

    if page.image_count:
        lines.extend(["", "## Figures", "", f"- figure count: `{page.image_count}`"])

    if page.concept_candidates:
        lines.extend(["", "## Concept candidates"])
        for concept in page.concept_candidates:
            lines.append(f"- {concept}")

    if page.rejected_concepts:
        lines.extend(["", "## Rejected concepts"])
        for concept in page.rejected_concepts:
            lines.append(
                f"- {concept.concept_name} | status={concept.status} | {concept.reason} "
                f"| confidence={concept.confidence_score} | evidence={concept.evidence_strength} "
                f"| definition={concept.definition_quality_score} | relevance={concept.interview_relevance}"
            )

    return "\n".join(lines).rstrip() + "\n"


def build_document_markdown(extraction: DocumentExtraction, relative_pdf: Path) -> str:
    lines = [
        "---",
        f'source_pdf: "{relative_pdf.as_posix()}"',
        f'course_id: "{extraction.course.course_id}"',
        f'course_name: "{extraction.course.course_name}"',
        f'category: "{extraction.course.category}"',
        f'semester: "{extraction.course.semester}"',
        f'title: "{extraction.title}"',
        f"page_count: {extraction.page_count}",
        f'parser_version: "{PARSER_VERSION}"',
        "---",
        "",
        f"# {extraction.title}",
        "",
        f"- source: `{relative_pdf.as_posix()}`",
        f"- pages: `{extraction.page_count}`",
    ]

    if extraction.warnings:
        lines.extend(["", "## Warnings"])
        for warning in extraction.warnings:
            lines.append(f"- {warning}")

    if extraction.metrics.total_pages_processed or extraction.metrics.candidate_concepts_generated:
        lines.extend(
            [
                "",
                "## Extraction metrics",
                f"- pages processed: `{extraction.metrics.total_pages_processed}`",
                f"- candidate concepts: `{extraction.metrics.candidate_concepts_generated}`",
                f"- concepts accepted: `{extraction.metrics.concepts_accepted}`",
                f"- concepts rejected: `{extraction.metrics.concepts_rejected}`",
                f"- rejected generic terms: `{extraction.metrics.rejected_generic_term}`",
                f"- rejected weak definitions: `{extraction.metrics.rejected_weak_definition}`",
                f"- rejected low depth: `{extraction.metrics.rejected_low_depth}`",
                f"- acceptance rate: `{extraction.metrics.acceptance_rate}`",
            ]
        )

    lines.extend(["", "## Page map"])
    for page in extraction.pages:
        lines.append(f"- page {page.page_number}: {page.heading or 'untitled'}")

    for page in extraction.pages:
        lines.extend(
            [
                "",
                f"## Page {page.page_number}" + (f": {page.heading}" if page.heading else ""),
                "",
                f"- source: `{relative_pdf.as_posix()}`",
                f"- page: `{page.page_number}`",
            ]
        )
        if page.extracted_text.strip():
            lines.extend(["", "### Extracted text", "", "```text", page.extracted_text.strip(), "```"])
        if page.tables:
            lines.append("")
            lines.append("### Tables")
            for index, table in enumerate(page.tables, start=1):
                table_md = table_to_markdown(table)
                if table_md:
                    lines.extend(["", f"#### Table {index}", "", table_md])
        if page.image_count:
            lines.extend(["", "### Figures", "", f"- figure count: `{page.image_count}`"])
        if page.concept_candidates:
            lines.extend(["", "### High-value concepts"])
            for concept in page.concept_candidates:
                lines.append(f"- {concept}")
        if page.candidate_concepts:
            lines.extend(["", "### Candidate concepts"])
            for concept in page.candidate_concepts:
                lines.append(
                    f"- {concept.concept_name} | type={concept.concept_type or 'concept'} | confidence={concept.confidence_score} "
                    f"| evidence={concept.evidence_strength} | definition={concept.definition_quality_score} "
                    f"| relevance={concept.interview_relevance} | {concept.reason_for_inclusion}"
                )
        if page.rejected_concepts:
            lines.extend(["", "### Rejected concepts"])
            for concept in page.rejected_concepts:
                lines.append(
                    f"- {concept.concept_name} | {concept.reason} | confidence={concept.confidence_score} "
                    f"| evidence={concept.evidence_strength} | definition={concept.definition_quality_score} "
                    f"| relevance={concept.interview_relevance}"
                )

    return "\n".join(lines).rstrip() + "\n"


def write_extraction_outputs(
    extraction: DocumentExtraction,
    processed_root: Path,
) -> dict[str, Path]:
    relative_pdf = extraction.relative_path
    stem_dir = Path(*relative_pdf.with_suffix("").parts)

    processed_doc_dir = processed_root / stem_dir
    processed_doc_dir.mkdir(parents=True, exist_ok=True)

    written: dict[str, Path] = {}

    document_md = build_document_markdown(extraction, relative_pdf)
    lecture_md_path = processed_doc_dir / "lecture.md"
    lecture_md_path.write_text(document_md, encoding="utf-8")
    written["lecture_md"] = lecture_md_path

    lecture_json_path = processed_doc_dir / "lecture.json"
    lecture_payload = {
        "pdf": relative_pdf.as_posix(),
        "course": asdict(extraction.course),
        "title": extraction.title,
        "page_count": extraction.page_count,
        "parser_version": PARSER_VERSION,
        "warnings": extraction.warnings,
        "metrics": asdict(extraction.metrics),
        "pages": [
            {
                "page_number": page.page_number,
                "heading": page.heading,
                "extracted_text": page.extracted_text,
                "tables": page.tables,
                "image_count": page.image_count,
                "concept_candidates": page.concept_candidates,
                "candidate_concepts": [asdict(candidate) for candidate in page.candidate_concepts],
                "rejected_concepts": [asdict(concept) for concept in page.rejected_concepts],
                "concepts": [asdict(concept) for concept in page.concepts],
            }
            for page in extraction.pages
        ],
    }
    lecture_json_path.write_text(json.dumps(lecture_payload, indent=2, ensure_ascii=True), encoding="utf-8")
    written["lecture_json"] = lecture_json_path
    written["lecture_dir"] = processed_doc_dir

    return written


def run_concept_filter(
    raw_root: Path,
    processed_root: Path,
    metadata_csv: Path,
    skill_bridge: PdfSkillBridge | None = None,
    pdf_paths: list[Path] | None = None,
) -> list[dict[str, object]]:
    metadata_rows = load_metadata(metadata_csv)
    pdfs = sorted(pdf_paths) if pdf_paths is not None else discover_pdfs(raw_root)
    results: list[dict[str, object]] = []

    bridge = skill_bridge or ExternalPdfSkillBridge()

    for pdf_path in pdfs:
        extraction = extract_pdf_document(pdf_path, raw_root, metadata_rows, bridge)
        written = write_extraction_outputs(extraction, processed_root)
        results.append(
            {
                "pdf": pdf_path.as_posix(),
                "course_id": extraction.course.course_id,
                "lecture_md": written["lecture_md"].as_posix(),
                "lecture_json": written["lecture_json"].as_posix(),
                "lecture_dir": written["lecture_dir"].as_posix(),
                "pages": len(extraction.pages),
                "candidate_concepts": extraction.metrics.candidate_concepts_generated,
                "concepts_accepted": extraction.metrics.concepts_accepted,
                "concepts_rejected": extraction.metrics.concepts_rejected,
            }
        )

    return results


def refilter_processed_lectures(
    processed_root: Path,
    course_ids: set[str] | None = None,
) -> list[dict[str, object]]:
    """Re-run concept selection against stored lecture JSON, without PDF parsing."""
    wanted = {str(value).strip() for value in (course_ids or set()) if str(value).strip()}
    results: list[dict[str, object]] = []
    graph_context = load_graph_context()

    for lecture_json_path in sorted(processed_root.rglob("lecture.json")):
        try:
            payload = json.loads(lecture_json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        raw_course = payload.get("course", {}) or {}
        course = CourseMetadata(
            course_id=str(raw_course.get("course_id", "") or ""),
            course_name=str(raw_course.get("course_name", "") or ""),
            category=str(raw_course.get("category", "") or ""),
            semester=str(raw_course.get("semester", "") or ""),
            folder=str(raw_course.get("folder", "") or ""),
            notes=str(raw_course.get("notes", "") or ""),
        )
        if wanted and course.course_id not in wanted:
            continue

        raw_pages = payload.get("pages", []) or []
        lecture_lines: list[str] = []
        for raw_page in raw_pages:
            lecture_lines.extend(normalize_lines(str(raw_page.get("extracted_text", "") or "")))
            heading = str(raw_page.get("heading", "") or "")
            if heading:
                lecture_lines.append(heading)
        lecture_context = normalize_spaces(" ".join(lecture_lines))
        normalized_pages: list[PageExtraction] = []
        extraction_metrics = ExtractionMetrics(total_pages_processed=len(raw_pages))

        for raw_page in raw_pages:
            page_number = int(raw_page.get("page_number", 0) or 0)
            text_lines = normalize_lines(str(raw_page.get("extracted_text", "") or ""))
            tables = raw_page.get("tables", []) or []
            candidate_details, concepts, rejected, page_metrics = build_structured_concepts(
                text_lines,
                str(raw_page.get("heading", "") or ""),
                tables,
                course,
                page_number,
                str(payload.get("pdf", "") or ""),
                # Reuse whole-lecture context so sparse slide definitions can
                # qualify when their evidence is distributed across pages.
                lecture_context=lecture_context,
                lecture_lines=lecture_lines,
                graph_context=graph_context,
            )
            for metric_name in (
                "candidate_concepts_generated",
                "concepts_accepted",
                "concepts_rejected",
                "rejected_low_confidence",
                "rejected_structural_noise",
                "rejected_ocr_noise",
                "rejected_generic_term",
                "rejected_weak_definition",
                "rejected_low_depth",
            ):
                setattr(extraction_metrics, metric_name, getattr(extraction_metrics, metric_name) + page_metrics[metric_name])
            normalized_pages.append(
                PageExtraction(
                    page_number=page_number,
                    heading=str(raw_page.get("heading", "") or ""),
                    extracted_text="\n".join(text_lines),
                    tables=tables,
                    image_count=int(raw_page.get("image_count", 0) or 0),
                    concept_candidates=[concept.concept_name for concept in concepts],
                    candidate_concepts=candidate_details,
                    rejected_concepts=rejected,
                    concepts=concepts,
                )
            )

        if extraction_metrics.candidate_concepts_generated:
            extraction_metrics.acceptance_rate = round(
                extraction_metrics.concepts_accepted / extraction_metrics.candidate_concepts_generated,
                3,
            )
        extraction = DocumentExtraction(
            pdf_path=Path(str(payload.get("pdf", "") or lecture_json_path.name)),
            relative_path=Path(str(payload.get("pdf", "") or lecture_json_path.name)),
            course=course,
            title=str(payload.get("title", "") or lecture_json_path.parent.name),
            page_count=int(payload.get("page_count", len(normalized_pages)) or len(normalized_pages)),
            pages=normalized_pages,
            warnings=[str(value) for value in (payload.get("warnings", []) or [])],
            metrics=extraction_metrics,
        )
        written = write_extraction_outputs(extraction, processed_root)
        results.append(
            {
                "lecture_json": lecture_json_path.as_posix(),
                "lecture_md": written["lecture_md"].as_posix(),
                "course_id": course.course_id,
                "pages": len(normalized_pages),
                "candidate_concepts": extraction_metrics.candidate_concepts_generated,
                "concepts_accepted": extraction_metrics.concepts_accepted,
                "concepts_rejected": extraction_metrics.concepts_rejected,
            }
        )
    return results


def extract_pdf_document(
    pdf_path: Path,
    raw_root: Path,
    metadata_rows: list[CourseMetadata],
    skill_bridge: PdfSkillBridge | None = None,
) -> DocumentExtraction:
    course = resolve_course(pdf_path, raw_root, metadata_rows)
    try:
        relative_pdf = pdf_path.relative_to(raw_root)
    except ValueError:
        relative_pdf = Path(pdf_path.name)

    bridge = skill_bridge or ExternalPdfSkillBridge()
    skill_result = bridge.extract(pdf_path)
    extraction = result_to_document_extraction(pdf_path, relative_pdf, course, skill_result)
    lecture_lines: list[str] = []
    for page in extraction.pages:
        lecture_lines.extend(normalize_lines(page.extracted_text))
        if page.heading:
            lecture_lines.append(page.heading)
    lecture_context = normalize_spaces(" ".join(lecture_lines))
    graph_context = load_graph_context()

    if not course.course_id and not course.course_name:
        extraction.warnings.append("no matching course metadata row found")

    normalized_pages: list[PageExtraction] = []
    extraction_metrics = ExtractionMetrics(total_pages_processed=len(extraction.pages))
    for page in extraction.pages:
        text_lines = normalize_lines(page.extracted_text)
        candidate_details, concepts, rejected_concepts, page_metrics = build_structured_concepts(
            text_lines,
            page.heading,
            page.tables,
            course,
            page.page_number,
            relative_pdf.as_posix(),
            lecture_context=lecture_context,
            lecture_lines=lecture_lines,
            graph_context=graph_context,
        )
        concept_candidates = [concept.concept_name for concept in concepts]
        extraction_metrics.candidate_concepts_generated += page_metrics["candidate_concepts_generated"]
        extraction_metrics.concepts_accepted += page_metrics["concepts_accepted"]
        extraction_metrics.concepts_rejected += page_metrics["concepts_rejected"]
        extraction_metrics.rejected_low_confidence += page_metrics["rejected_low_confidence"]
        extraction_metrics.rejected_structural_noise += page_metrics["rejected_structural_noise"]
        extraction_metrics.rejected_ocr_noise += page_metrics["rejected_ocr_noise"]
        extraction_metrics.rejected_generic_term += page_metrics["rejected_generic_term"]
        extraction_metrics.rejected_weak_definition += page_metrics["rejected_weak_definition"]
        extraction_metrics.rejected_low_depth += page_metrics["rejected_low_depth"]
        normalized_pages.append(
            PageExtraction(
                page_number=page.page_number,
                heading=page.heading,
                extracted_text="\n".join(text_lines),
                tables=page.tables,
                image_count=page.image_count,
                concept_candidates=concept_candidates,
                candidate_concepts=candidate_details,
                rejected_concepts=rejected_concepts,
                concepts=concepts,
            )
        )

    extraction.pages = normalized_pages
    extraction.metrics = extraction_metrics
    if extraction_metrics.candidate_concepts_generated:
        extraction.metrics.acceptance_rate = round(
            extraction_metrics.concepts_accepted / extraction_metrics.candidate_concepts_generated,
            3,
        )
    if not extraction.title:
        extraction.title = course.course_name or pdf_path.stem
    if extraction.page_count <= 0:
        extraction.page_count = len(extraction.pages)
    return extraction
