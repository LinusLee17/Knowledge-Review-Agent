from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


_SCOPE_LEVEL_BY_TYPE = {
    "framework": 5,
    "workflow": 4,
    "theory": 4,
    "model": 3,
    "algorithm": 3,
    "method": 3,
    "theorem": 3,
    "principle": 3,
    "process": 3,
    "metric": 1,
    "concept": 2,
    "phenomenon": 2,
    "practice": 2,
    "skill": 2,
}


def infer_scope_level(concept_type: str = "", concept_name: str = "", topic: str = "") -> int:
    """Return structural breadth, separate from educational value."""
    normalized_type = str(concept_type or "").strip().lower()
    if normalized_type in _SCOPE_LEVEL_BY_TYPE:
        return _SCOPE_LEVEL_BY_TYPE[normalized_type]

    normalized_name = str(concept_name or "").strip().lower()
    if normalized_name in {"regression", "classification", "inference", "optimization", "analytics"}:
        return 4
    if str(topic or "").strip() and normalized_name == str(topic).strip().lower():
        return 4
    return 3


@dataclass(frozen=True)
class CourseMetadata:
    course_id: str = ""
    course_name: str = ""
    category: str = ""
    semester: str = ""
    folder: str = ""
    notes: str = ""


@dataclass
class PageExtraction:
    page_number: int
    heading: str
    extracted_text: str
    tables: list[list[list[str]]] = field(default_factory=list)
    image_count: int = 0
    concept_candidates: list[str] = field(default_factory=list)
    candidate_concepts: list["ConceptCandidate"] = field(default_factory=list)
    rejected_concepts: list["RejectedConcept"] = field(default_factory=list)
    concepts: list["ConceptExtraction"] = field(default_factory=list)


@dataclass(frozen=True)
class ConceptCandidate:
    concept_name: str
    confidence_score: float
    concept_type: str = ""
    evidence_strength: float = 0.0
    definition_quality_score: float = 0.0
    interview_relevance: float = 0.0
    reason_for_inclusion: str = ""
    domain: str = ""
    topic: str = ""
    importance_score: int = 1
    scope_level: int = 0
    study_priority: int = 0
    evidence: str = ""
    aliases: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RejectedConcept:
    concept_name: str
    status: str = "rejected"
    reason: str = ""
    concept_type: str = ""
    confidence_score: float = 0.0
    evidence_strength: float = 0.0
    definition_quality_score: float = 0.0
    interview_relevance: float = 0.0
    domain: str = ""
    topic: str = ""
    evidence: str = ""


@dataclass
class ExtractionMetrics:
    total_pages_processed: int = 0
    candidate_concepts_generated: int = 0
    concepts_accepted: int = 0
    concepts_rejected: int = 0
    rejected_structural_noise: int = 0
    rejected_ocr_noise: int = 0
    rejected_low_confidence: int = 0
    rejected_generic_term: int = 0
    rejected_weak_definition: int = 0
    rejected_low_depth: int = 0
    acceptance_rate: float = 0.0


@dataclass(frozen=True)
class ConceptExtraction:
    concept_name: str
    concept_type: str = ""
    domain: str = ""
    topic: str = ""
    importance_score: int = 1
    scope_level: int = 0
    study_priority: int = 0
    confidence_score: float = 0.0
    confidence_reason: str = ""
    evidence_strength: float = 0.0
    definition_quality_score: float = 0.0
    interview_relevance: float = 0.0
    reason_for_inclusion: str = ""
    definition: str = ""
    intuition: str = ""
    mathematical_foundation: str = ""
    assumptions: list[str] = field(default_factory=list)
    applications: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    advantages: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    related_concepts: list[str] = field(default_factory=list)
    broader_topics: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    canonical_key: str = ""
    evidence: str = ""
    source: dict[str, str] = field(default_factory=dict)


@dataclass
class DocumentExtraction:
    pdf_path: Path
    relative_path: Path
    course: CourseMetadata
    title: str
    page_count: int
    pages: list[PageExtraction] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: ExtractionMetrics = field(default_factory=ExtractionMetrics)


@dataclass
class RepositoryIndexEntry:
    filename: str
    relative_file_path: str
    sha256: str
    processing_status: str
    processing_timestamp: str
    source_course: str = ""
    source_lecture: str = ""
    output_location: str = ""
    parser_version: str = ""
    outputs: dict[str, str] = field(default_factory=dict)
    previous_relative_paths: list[str] = field(default_factory=list)
    last_seen_timestamp: str = ""
    page_count: int = 0


@dataclass
class RepositoryIndex:
    schema_version: int = 1
    parser_version: str = ""
    generated_at: str = ""
    entries: list[RepositoryIndexEntry] = field(default_factory=list)


@dataclass
class IngestionResult:
    processed: list[RepositoryIndexEntry] = field(default_factory=list)
    skipped: list[RepositoryIndexEntry] = field(default_factory=list)
    errors: list[RepositoryIndexEntry] = field(default_factory=list)


@dataclass(frozen=True)
class ConceptMetadata:
    concept_name: str
    canonical_key: str = ""
    concept_type: str = ""
    domain: str = ""
    topic: str = ""
    importance_score: int = 1
    scope_level: int = 0
    study_priority: int = 0
    confidence_score: float = 0.0
    evidence_strength: float = 0.0
    definition_quality_score: float = 0.0
    interview_relevance: float = 0.0
    definition: str = ""
    intuition: str = ""
    mathematical_foundation: str = ""
    advantages: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    applications: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    broader_topics: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    contributing_courses: list[str] = field(default_factory=list)
    contributing_lecture_files: list[str] = field(default_factory=list)
    source_lecture_hashes: dict[str, str] = field(default_factory=dict)
    last_updated_timestamp: str = ""
    version_number: int = 1
    related_concepts: list[str] = field(default_factory=list)
    prerequisites: list[str] = field(default_factory=list)
    used_in: list[str] = field(default_factory=list)
    graph_node_id: str = ""

    def __post_init__(self) -> None:
        if self.scope_level <= 0:
            object.__setattr__(self, "scope_level", infer_scope_level(self.concept_type, self.concept_name, self.topic))
        if self.study_priority <= 0:
            object.__setattr__(self, "study_priority", max(1, min(5, self.importance_score or 1)))


@dataclass(frozen=True)
class GraphNode:
    node_id: str
    concept_key: str
    concept_name: str
    metadata_path: str
    version_number: int
    last_updated_timestamp: str
    domain: str = ""
    topic: str = ""
    importance_score: int = 1
    scope_level: int = 3
    study_priority: int = 1
    contributing_courses: list[str] = field(default_factory=list)
    contributing_lecture_files: list[str] = field(default_factory=list)
    graph_node_id: str = ""


@dataclass(frozen=True)
class GraphEdge:
    edge_id: str
    source_node_id: str
    source_concept_key: str
    target_node_id: str
    target_concept_key: str
    relation_type: str
    target_resolved: bool = False
    source_concept_name: str = ""
    target_concept_name: str = ""
    source_metadata_path: str = ""
    source_version_number: int = 0
    supporting_concept_keys: list[str] = field(default_factory=list)
    supporting_metadata_paths: list[str] = field(default_factory=list)
    supporting_courses: list[str] = field(default_factory=list)
    supporting_lecture_files: list[str] = field(default_factory=list)
    supporting_lecture_hashes: dict[str, str] = field(default_factory=dict)
    last_updated_timestamp: str = ""


@dataclass
class GraphState:
    schema_version: int = 1
    generated_at: str = ""
    node_fingerprints: dict[str, str] = field(default_factory=dict)
    edge_fingerprints: dict[str, str] = field(default_factory=dict)
    concept_node_ids: dict[str, str] = field(default_factory=dict)


@dataclass
class GraphBuildReport:
    nodes_created: list[str] = field(default_factory=list)
    nodes_updated: list[str] = field(default_factory=list)
    nodes_unchanged: list[str] = field(default_factory=list)
    nodes_deleted: list[str] = field(default_factory=list)
    edges_created: list[str] = field(default_factory=list)
    edges_updated: list[str] = field(default_factory=list)
    edges_unchanged: list[str] = field(default_factory=list)
    edges_deleted: list[str] = field(default_factory=list)
    unresolved_edge_targets: int = 0
    concepts_processed: int = 0
