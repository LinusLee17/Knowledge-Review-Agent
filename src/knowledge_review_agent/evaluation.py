from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .consolidation import discover_concept_records
from .concept_rules import (
    canonical_common_mistakes_for_label,
    canonical_common_variants_for_label,
    canonical_connections_for_label,
    canonical_further_reading_for_label,
    canonical_intuition_for_label,
    canonical_how_it_works_for_label,
    canonical_interview_questions_for_label,
    canonical_key_components_for_label,
    canonical_math_for_label,
    canonical_why_it_matters_for_label,
)
from .utils import normalize_concept_key, normalize_spaces


@dataclass(frozen=True)
class ConsolidationEvaluation:
    concept_count: int
    duplicate_key_groups: int
    duplicate_concept_dirs: int
    concepts_with_provenance: int
    concepts_with_multi_course_provenance: int
    concepts_with_domain_topic: int
    high_importance_concepts: int
    medium_importance_concepts: int
    low_importance_concepts: int
    average_importance_score: float
    average_courses_per_concept: float
    average_lecture_files_per_concept: float
    relation_link_count: int
    orphan_concept_directories: int
    semantic_usefulness_score: float
    specificity_score: float
    explanation_quality_score: float
    depth_score: float
    generic_term_penalty_count: int
    weak_definition_concepts: int
    low_depth_concepts: int
    heuristic_merge_score: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _directory_health(concepts_root: Path) -> int:
    if not concepts_root.exists():
        return 0
    orphan_count = 0
    for directory in concepts_root.iterdir():
        if not directory.is_dir():
            continue
        concept_md = directory / "concept.md"
        metadata_json = directory / "metadata.json"
        if concept_md.exists() and metadata_json.exists():
            continue
        orphan_count += 1
    return orphan_count


_GENERIC_CONCEPT_KEYS = {
    normalize_concept_key(value)
    for value in ("accuracy", "prediction", "model", "training", "feature", "data", "classification", "regression")
}


def _best_entry(entries: list) -> object:
    return sorted(
        entries,
        key=lambda entry: (
            entry.metadata.version_number,
            entry.metadata.last_updated_timestamp,
            str(entry.directory),
        ),
        reverse=True,
    )[0]


def _section_population(metadata) -> int:
    sections = [
        metadata.definition,
        canonical_why_it_matters_for_label(metadata.concept_name),
        metadata.intuition or canonical_intuition_for_label(metadata.concept_name),
        metadata.mathematical_foundation or canonical_math_for_label(metadata.concept_name),
        canonical_how_it_works_for_label(metadata.concept_name),
        ", ".join(canonical_key_components_for_label(metadata.concept_name)),
        ", ".join(metadata.advantages or []),
        ", ".join(metadata.limitations or []),
        ", ".join(canonical_common_mistakes_for_label(metadata.concept_name)),
        ", ".join(canonical_common_variants_for_label(metadata.concept_name)),
        ", ".join(metadata.applications or []),
        ", ".join(canonical_interview_questions_for_label(metadata.concept_name)),
        ", ".join(metadata.related_concepts or []),
        ", ".join(metadata.prerequisites or []),
        ", ".join(canonical_connections_for_label(metadata.concept_name)),
        ", ".join(metadata.broader_topics or []),
        ", ".join(canonical_further_reading_for_label(metadata.concept_name)),
    ]
    return sum(1 for value in sections if normalize_spaces(str(value or "")))


def _is_generic_concept(name: str) -> bool:
    return normalize_concept_key(name) in _GENERIC_CONCEPT_KEYS


def _definition_quality(metadata) -> float:
    definition = normalize_spaces(metadata.definition)
    if not definition:
        return 0.0
    if normalize_concept_key(definition) == normalize_concept_key(metadata.concept_name):
        return 0.25 if len(definition.split()) <= 3 else 0.35
    score = 0.45
    if len(definition.split()) >= 8:
        score += 0.2
    if any(cue in definition.lower() for cue in (" model ", " method ", " algorithm ", " metric ", " estimates ", " measures ", " predicts ", " relationship ")):
        score += 0.15
    if metadata.mathematical_foundation:
        score += 0.1
    return min(1.0, score)


def _specificity(metadata) -> float:
    score = 1.0
    if _is_generic_concept(metadata.concept_name):
        score -= 0.35
    if not metadata.domain or not metadata.topic:
        score -= 0.15
    if len(metadata.aliases or []) <= 1:
        score -= 0.05
    return max(0.0, min(1.0, score))


def _usefulness(metadata, courses: set[str], lecture_files: set[str]) -> float:
    score = 0.0
    score += min(1.0, (metadata.importance_score or 1) / 5.0) * 0.45
    score += 0.2 if courses else 0.0
    score += 0.15 if len(courses) > 1 else 0.0
    score += 0.1 if metadata.applications else 0.0
    score += 0.05 if metadata.related_concepts else 0.0
    score += 0.05 if metadata.prerequisites else 0.0
    return max(0.0, min(1.0, score))


def evaluate_consolidation(concepts_root: Path) -> ConsolidationEvaluation:
    records = discover_concept_records(concepts_root)
    grouped: dict[str, list] = {}
    for record in records:
        grouped.setdefault(record.key, []).append(record)

    concept_count = len(grouped)
    duplicate_key_groups = sum(1 for entries in grouped.values() if len(entries) > 1)
    duplicate_concept_dirs = sum(len(entries) - 1 for entries in grouped.values() if len(entries) > 1)

    concepts_with_provenance = 0
    concepts_with_multi_course_provenance = 0
    concepts_with_domain_topic = 0
    high_importance_concepts = 0
    medium_importance_concepts = 0
    low_importance_concepts = 0
    total_courses = 0
    total_lecture_files = 0
    total_importance = 0
    relation_link_count = 0
    total_usefulness = 0.0
    total_specificity = 0.0
    total_explanation_quality = 0.0
    total_depth = 0.0
    generic_term_penalty_count = 0
    weak_definition_concepts = 0
    low_depth_concepts = 0

    for entries in grouped.values():
        best = _best_entry(entries)
        metadata = best.metadata
        courses = set()
        lecture_files = set()
        domain = ""
        topic = ""
        importance_score = 1
        relation_targets = set()
        for entry in entries:
            courses.update(entry.metadata.contributing_courses)
            lecture_files.update(entry.metadata.contributing_lecture_files)
            if entry.metadata.domain:
                domain = entry.metadata.domain
            if entry.metadata.topic:
                topic = entry.metadata.topic
            importance_score = max(importance_score, entry.metadata.importance_score or 1)
            relation_targets.update(entry.metadata.related_concepts)
            relation_targets.update(entry.metadata.prerequisites)
            relation_targets.update(entry.metadata.used_in)
            relation_targets.update(entry.metadata.applications)
        if courses or lecture_files:
            concepts_with_provenance += 1
        if len(courses) > 1:
            concepts_with_multi_course_provenance += 1
        if domain and topic:
            concepts_with_domain_topic += 1
        if importance_score >= 4:
            high_importance_concepts += 1
        elif importance_score >= 3:
            medium_importance_concepts += 1
        else:
            low_importance_concepts += 1
        total_courses += len(courses)
        total_lecture_files += len(lecture_files)
        total_importance += importance_score
        relation_link_count += len({target for target in relation_targets if target})
        usefulness = _usefulness(metadata, courses, lecture_files)
        specificity = _specificity(metadata)
        explanation_quality = _definition_quality(metadata)
        depth = min(1.0, _section_population(metadata) / 5.0)
        total_usefulness += usefulness
        total_specificity += specificity
        total_explanation_quality += explanation_quality
        total_depth += depth
        if _is_generic_concept(metadata.concept_name):
            generic_term_penalty_count += 1
        if explanation_quality < 0.55:
            weak_definition_concepts += 1
        if depth < 0.6:
            low_depth_concepts += 1

    orphan_concept_directories = _directory_health(concepts_root)
    denominator = max(concept_count, 1)
    provenance_ratio = concepts_with_provenance / denominator
    multi_course_ratio = concepts_with_multi_course_provenance / denominator
    domain_topic_ratio = concepts_with_domain_topic / denominator
    high_importance_ratio = high_importance_concepts / denominator
    relation_density = min(1.0, relation_link_count / max(concept_count * 4, 1))
    dedupe_ratio = 1.0 - (duplicate_concept_dirs / denominator)
    if concepts_root.exists():
        concept_root_entries = list(concepts_root.iterdir())
        completeness_ratio = 1.0 - (orphan_concept_directories / max(len(concept_root_entries), 1))
    else:
        completeness_ratio = 1.0
    average_importance_score = round(total_importance / denominator, 3)
    semantic_usefulness_score = round(total_usefulness / denominator, 3)
    specificity_score = round(total_specificity / denominator, 3)
    explanation_quality_score = round(total_explanation_quality / denominator, 3)
    depth_score = round(total_depth / denominator, 3)
    heuristic_merge_score = round(
        max(
            0.0,
            min(
                100.0,
                100.0 * (
                    0.25 * provenance_ratio
                    + 0.20 * dedupe_ratio
                    + 0.20 * completeness_ratio
                    + 0.20 * domain_topic_ratio
                    + 0.15 * high_importance_ratio
                    + 0.08 * semantic_usefulness_score
                    + 0.08 * specificity_score
                    + 0.08 * explanation_quality_score
                    + 0.08 * depth_score
                    - 0.05 * (generic_term_penalty_count / denominator)
                ),
            ),
        ),
        2,
    )

    return ConsolidationEvaluation(
        concept_count=concept_count,
        duplicate_key_groups=duplicate_key_groups,
        duplicate_concept_dirs=duplicate_concept_dirs,
        concepts_with_provenance=concepts_with_provenance,
        concepts_with_multi_course_provenance=concepts_with_multi_course_provenance,
        concepts_with_domain_topic=concepts_with_domain_topic,
        high_importance_concepts=high_importance_concepts,
        medium_importance_concepts=medium_importance_concepts,
        low_importance_concepts=low_importance_concepts,
        average_importance_score=average_importance_score,
        average_courses_per_concept=round(total_courses / denominator, 3),
        average_lecture_files_per_concept=round(total_lecture_files / denominator, 3),
        relation_link_count=relation_link_count,
        orphan_concept_directories=orphan_concept_directories,
        semantic_usefulness_score=semantic_usefulness_score,
        specificity_score=specificity_score,
        explanation_quality_score=explanation_quality_score,
        depth_score=depth_score,
        generic_term_penalty_count=generic_term_penalty_count,
        weak_definition_concepts=weak_definition_concepts,
        low_depth_concepts=low_depth_concepts,
        heuristic_merge_score=heuristic_merge_score,
    )
