from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .models import ConceptMetadata
from .utils import canonical_concept_name, normalize_concept_key


def concept_directory(concepts_root: Path, concept_name: str) -> Path:
    safe_name = concept_name.strip().replace("/", "-").replace("\\", "-")
    return concepts_root / safe_name


def concept_paths(concepts_root: Path, concept_name: str) -> tuple[Path, Path]:
    directory = concept_directory(concepts_root, concept_name)
    return directory / "concept.md", directory / "metadata.json"


def load_concept_metadata(metadata_path: Path) -> ConceptMetadata | None:
    if not metadata_path.exists():
        return None
    payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    return ConceptMetadata(
        concept_name=str(payload.get("concept_name", "") or ""),
        canonical_key=str(payload.get("canonical_key", "") or ""),
        concept_type=str(payload.get("concept_type", "") or ""),
        domain=str(payload.get("domain", "") or ""),
        topic=str(payload.get("topic", "") or ""),
        importance_score=int(payload.get("importance_score", 1) or 1),
        confidence_score=float(payload.get("confidence_score", 0.0) or 0.0),
        evidence_strength=float(payload.get("evidence_strength", 0.0) or 0.0),
        definition_quality_score=float(payload.get("definition_quality_score", 0.0) or 0.0),
        interview_relevance=float(payload.get("interview_relevance", 0.0) or 0.0),
        definition=str(payload.get("definition", "") or ""),
        intuition=str(payload.get("intuition", "") or ""),
        mathematical_foundation=str(payload.get("mathematical_foundation", "") or ""),
        advantages=list(payload.get("advantages", []) or []),
        assumptions=list(payload.get("assumptions", []) or []),
        applications=list(payload.get("applications", []) or []),
        limitations=list(payload.get("limitations", []) or []),
        broader_topics=list(payload.get("broader_topics", []) or []),
        aliases=list(payload.get("aliases", []) or []),
        contributing_courses=list(payload.get("contributing_courses", []) or []),
        contributing_lecture_files=list(payload.get("contributing_lecture_files", []) or []),
        source_lecture_hashes=dict(payload.get("source_lecture_hashes", {}) or {}),
        last_updated_timestamp=str(payload.get("last_updated_timestamp", "") or ""),
        version_number=int(payload.get("version_number", 1) or 1),
        related_concepts=list(payload.get("related_concepts", []) or []),
        prerequisites=list(payload.get("prerequisites", []) or []),
        used_in=list(payload.get("used_in", []) or []),
        graph_node_id=str(payload.get("graph_node_id", "") or ""),
    )


def save_concept_metadata(metadata_path: Path, metadata: ConceptMetadata) -> None:
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    canonical_key = metadata.canonical_key or normalize_concept_key(metadata.concept_name)
    metadata = ConceptMetadata(
        concept_name=metadata.concept_name,
        canonical_key=canonical_key,
        concept_type=metadata.concept_type,
        domain=metadata.domain,
        topic=metadata.topic,
        importance_score=metadata.importance_score,
        confidence_score=metadata.confidence_score,
        evidence_strength=metadata.evidence_strength,
        definition_quality_score=metadata.definition_quality_score,
        interview_relevance=metadata.interview_relevance,
        definition=metadata.definition,
        intuition=metadata.intuition,
        mathematical_foundation=metadata.mathematical_foundation,
        advantages=sorted(set(metadata.advantages)),
        assumptions=sorted(set(metadata.assumptions)),
        applications=sorted(set(metadata.applications)),
        limitations=sorted(set(metadata.limitations)),
        broader_topics=sorted(set(metadata.broader_topics)),
        aliases=sorted(set(metadata.aliases)),
        contributing_courses=sorted(set(metadata.contributing_courses)),
        contributing_lecture_files=sorted(set(metadata.contributing_lecture_files)),
        source_lecture_hashes=dict(sorted(metadata.source_lecture_hashes.items())),
        last_updated_timestamp=metadata.last_updated_timestamp or datetime.now(timezone.utc).isoformat(),
        version_number=metadata.version_number,
        related_concepts=sorted(set(metadata.related_concepts)),
        prerequisites=sorted(set(metadata.prerequisites)),
        used_in=sorted(set(metadata.used_in)),
        graph_node_id=metadata.graph_node_id,
    )
    metadata_path.write_text(json.dumps(asdict(metadata), indent=2, ensure_ascii=True), encoding="utf-8")


def load_concept_key(metadata_path: Path) -> str:
    metadata = load_concept_metadata(metadata_path)
    if not metadata:
        return ""
    return metadata.canonical_key or normalize_concept_key(metadata.concept_name)


def concept_display_name_from_key(key: str) -> str:
    return canonical_concept_name(key) or key
