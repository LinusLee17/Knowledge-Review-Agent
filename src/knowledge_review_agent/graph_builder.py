from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .concept_store import concept_display_name_from_key
from .consolidation import discover_concept_records
from .graph_store import (
    load_graph_state,
    save_graph_edges,
    save_graph_nodes,
    save_graph_state,
    stable_fingerprint,
)
from .models import ConceptMetadata, GraphBuildReport, GraphEdge, GraphNode, GraphState
from .utils import normalize_concept_key, normalize_spaces, slugify


@dataclass(frozen=True)
class GraphConceptRecord:
    key: str
    directory: Path
    metadata_path: Path
    metadata: ConceptMetadata


@dataclass(frozen=True)
class EdgeSpec:
    relation_type: str
    source_key: str
    target_key: str
    source_record: GraphConceptRecord
    target_resolved: bool


def _choose_primary_record(records: list[GraphConceptRecord]) -> GraphConceptRecord:
    return sorted(
        records,
        key=lambda record: (
            record.metadata.version_number,
            record.metadata.last_updated_timestamp,
            str(record.directory),
        ),
        reverse=True,
    )[0]


def _merge_records(records: list[GraphConceptRecord]) -> GraphConceptRecord:
    primary = _choose_primary_record(records)
    merged_courses = sorted(set().union(*(record.metadata.contributing_courses for record in records)))
    merged_lecture_files = sorted(set().union(*(record.metadata.contributing_lecture_files for record in records)))
    merged_hashes: dict[str, str] = {}
    merged_related = sorted(set().union(*(record.metadata.related_concepts for record in records)))
    merged_prereqs = sorted(set().union(*(record.metadata.prerequisites for record in records)))
    merged_used_in = sorted(set().union(*(record.metadata.used_in for record in records)))
    merged_applications = sorted(set().union(*(record.metadata.applications for record in records)))
    merged_broader_topics = sorted(set().union(*(record.metadata.broader_topics for record in records)))
    merged_aliases = sorted(set().union(*(record.metadata.aliases for record in records)))

    for record in records:
        merged_hashes.update(record.metadata.source_lecture_hashes or {})

    def _best_text(attr: str, fallback: str = "") -> str:
        values = [getattr(record.metadata, attr, "") for record in records]
        values = [str(value).strip() for value in values if str(value).strip()]
        if not values:
            return fallback
        from collections import Counter

        counts = Counter(values)
        best_count = max(counts.values())
        candidates = [value for value, count in counts.items() if count == best_count]
        candidates.sort(key=lambda value: (-len(value), value.lower()))
        return candidates[0]

    merged_metadata = ConceptMetadata(
        concept_name=primary.metadata.concept_name or concept_display_name_from_key(primary.key),
        canonical_key=primary.metadata.canonical_key or primary.key,
        domain=_best_text("domain", primary.metadata.domain),
        topic=_best_text("topic", primary.metadata.topic),
        importance_score=max(record.metadata.importance_score for record in records),
        scope_level=max(record.metadata.scope_level for record in records),
        study_priority=max(record.metadata.study_priority for record in records),
        definition=_best_text("definition", primary.metadata.definition),
        intuition=_best_text("intuition", primary.metadata.intuition),
        mathematical_foundation=_best_text("mathematical_foundation", primary.metadata.mathematical_foundation),
        advantages=sorted(set().union(*(record.metadata.advantages for record in records))),
        assumptions=sorted(set().union(*(record.metadata.assumptions for record in records))),
        applications=merged_applications,
        limitations=sorted(set().union(*(record.metadata.limitations for record in records))),
        broader_topics=merged_broader_topics,
        aliases=merged_aliases,
        contributing_courses=merged_courses,
        contributing_lecture_files=merged_lecture_files,
        source_lecture_hashes=merged_hashes,
        last_updated_timestamp=max(
            (record.metadata.last_updated_timestamp for record in records if record.metadata.last_updated_timestamp),
            default=primary.metadata.last_updated_timestamp,
        ),
        version_number=max(record.metadata.version_number for record in records),
        related_concepts=merged_related,
        prerequisites=merged_prereqs,
        used_in=merged_used_in,
        graph_node_id=primary.metadata.graph_node_id or slugify(primary.key),
    )
    return GraphConceptRecord(
        key=primary.key,
        directory=primary.directory,
        metadata_path=primary.metadata_path,
        metadata=merged_metadata,
    )


def _group_records_by_key(records: Iterable) -> dict[str, list[GraphConceptRecord]]:
    grouped: dict[str, list[GraphConceptRecord]] = defaultdict(list)
    for record in records:
        key = record.key if record.key else normalize_concept_key(record.metadata.concept_name)
        if not key:
            continue
        grouped[key].append(
            GraphConceptRecord(
                key=key,
                directory=record.directory,
                metadata_path=record.metadata_path,
                metadata=record.metadata,
            )
        )
    return grouped


def _graph_root_files(graphs_root: Path) -> tuple[Path, Path, Path, Path]:
    nodes_path = graphs_root / "nodes.json"
    edges_path = graphs_root / "edges.json"
    state_path = graphs_root / "state.json"
    delta_dir = graphs_root / "deltas"
    return nodes_path, edges_path, state_path, delta_dir


def _node_id_for_record(record: GraphConceptRecord) -> str:
    return record.metadata.graph_node_id or slugify(record.key)


def _build_node(record: GraphConceptRecord) -> GraphNode:
    node_id = _node_id_for_record(record)
    return GraphNode(
        node_id=node_id,
        concept_key=record.key,
        concept_name=record.metadata.concept_name or concept_display_name_from_key(record.key),
        metadata_path=record.metadata_path.as_posix(),
        version_number=record.metadata.version_number,
        last_updated_timestamp=record.metadata.last_updated_timestamp,
        domain=record.metadata.domain,
        topic=record.metadata.topic,
        importance_score=record.metadata.importance_score,
        scope_level=record.metadata.scope_level,
        study_priority=record.metadata.study_priority,
        contributing_courses=sorted(set(record.metadata.contributing_courses)),
        contributing_lecture_files=sorted(set(record.metadata.contributing_lecture_files)),
        graph_node_id=node_id,
    )


def _relation_targets(metadata: ConceptMetadata) -> list[tuple[str, str]]:
    targets: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for target in metadata.prerequisites:
        key = normalize_concept_key(target)
        if not key:
            continue
        spec = ("prerequisite", key)
        if spec not in seen:
            seen.add(spec)
            targets.append(spec)

    for target in metadata.related_concepts:
        key = normalize_concept_key(target)
        if not key:
            continue
        spec = ("related", key)
        if spec not in seen:
            seen.add(spec)
            targets.append(spec)

    return targets


def _alias_candidates(record: GraphConceptRecord) -> list[str]:
    aliases: list[str] = [
        record.key,
        record.metadata.canonical_key,
        record.metadata.concept_name,
        record.metadata.graph_node_id,
        *(record.metadata.aliases or []),
    ]
    profile = record.metadata.concept_name and concept_display_name_from_key(record.key)
    if profile:
        aliases.append(profile)
    return [alias for alias in aliases if normalize_spaces(alias)]


def _alias_lookup(records: dict[str, GraphConceptRecord]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for key, record in records.items():
        for alias in _alias_candidates(record):
            normalized = normalize_concept_key(alias)
            if normalized and normalized not in lookup:
                lookup[normalized] = key
    return lookup


def _edge_identity(relation_type: str, source_key: str, target_key: str) -> tuple[str, str, str]:
    if relation_type == "related":
        ordered = sorted([source_key, target_key])
        return relation_type, ordered[0], ordered[1]
    return relation_type, source_key, target_key


def _edge_id(relation_type: str, source_key: str, target_key: str) -> str:
    relation_type, left, right = _edge_identity(relation_type, source_key, target_key)
    return f"{relation_type}::{left}::{right}"


def _edge_payload_for_spec(
    spec: EdgeSpec,
    node_lookup: dict[str, GraphNode],
) -> GraphEdge:
    relation_type, left_key, right_key = _edge_identity(spec.relation_type, spec.source_key, spec.target_key)
    if relation_type == "related":
        source_key = left_key
        target_key = right_key
    else:
        source_key = spec.source_key
        target_key = spec.target_key

    source_node = node_lookup.get(source_key)
    target_node = node_lookup.get(target_key)
    source_node_id = source_node.node_id if source_node else slugify(source_key)
    target_node_id = target_node.node_id if target_node else slugify(target_key)
    target_resolved = target_node is not None

    metadata = spec.source_record.metadata
    supporting_lecture_hashes = {
        lecture_file: lecture_hash
        for lecture_file, lecture_hash in sorted((metadata.source_lecture_hashes or {}).items())
    }

    return GraphEdge(
        edge_id=_edge_id(relation_type, source_key, target_key),
        source_node_id=source_node_id,
        source_concept_key=source_key,
        target_node_id=target_node_id,
        target_concept_key=target_key,
        relation_type=relation_type,
        target_resolved=target_resolved,
        source_concept_name=spec.source_record.metadata.concept_name or concept_display_name_from_key(source_key),
        target_concept_name=target_node.concept_name if target_node else concept_display_name_from_key(target_key),
        source_metadata_path=spec.source_record.metadata_path.as_posix(),
        source_version_number=metadata.version_number,
        supporting_concept_keys=[spec.source_key],
        supporting_metadata_paths=[spec.source_record.metadata_path.as_posix()],
        supporting_courses=sorted(set(metadata.contributing_courses)),
        supporting_lecture_files=sorted(set(metadata.contributing_lecture_files)),
        supporting_lecture_hashes=supporting_lecture_hashes,
        last_updated_timestamp=metadata.last_updated_timestamp,
    )


def _build_edge_specs(
    records: dict[str, GraphConceptRecord],
    node_lookup: dict[str, GraphNode],
    alias_lookup: dict[str, str],
) -> list[EdgeSpec]:
    specs: list[EdgeSpec] = []
    for source_key, record in records.items():
        for relation_type, target_key in _relation_targets(record.metadata):
            resolved_target = alias_lookup.get(target_key, "")
            if not resolved_target or resolved_target == source_key:
                continue
            target_resolved = target_key in node_lookup
            if not target_resolved:
                continue
            specs.append(
                EdgeSpec(
                    relation_type=relation_type,
                    source_key=source_key,
                    target_key=resolved_target,
                    source_record=record,
                    target_resolved=resolved_target in node_lookup,
                )
            )
    return specs


def _merge_edges(specs: list[EdgeSpec], node_lookup: dict[str, GraphNode]) -> list[GraphEdge]:
    grouped: dict[str, GraphEdge] = {}
    for spec in specs:
        payload = _edge_payload_for_spec(spec, node_lookup)
        existing = grouped.get(payload.edge_id)
        if not existing:
            grouped[payload.edge_id] = payload
            continue

        grouped[payload.edge_id] = GraphEdge(
            edge_id=payload.edge_id,
            source_node_id=existing.source_node_id,
            source_concept_key=existing.source_concept_key,
            target_node_id=existing.target_node_id,
            target_concept_key=existing.target_concept_key,
            relation_type=existing.relation_type,
            target_resolved=existing.target_resolved or payload.target_resolved,
            source_concept_name=existing.source_concept_name,
            target_concept_name=existing.target_concept_name,
            source_metadata_path=existing.source_metadata_path,
            source_version_number=max(existing.source_version_number, payload.source_version_number),
            supporting_concept_keys=sorted(set(existing.supporting_concept_keys + payload.supporting_concept_keys)),
            supporting_metadata_paths=sorted(
                set(existing.supporting_metadata_paths + payload.supporting_metadata_paths)
            ),
            supporting_courses=sorted(set(existing.supporting_courses + payload.supporting_courses)),
            supporting_lecture_files=sorted(
                set(existing.supporting_lecture_files + payload.supporting_lecture_files)
            ),
            supporting_lecture_hashes={
                **existing.supporting_lecture_hashes,
                **payload.supporting_lecture_hashes,
            },
            last_updated_timestamp=max(existing.last_updated_timestamp, payload.last_updated_timestamp),
        )
    return sorted(grouped.values(), key=lambda edge: edge.edge_id)


def build_knowledge_graph(concepts_root: Path, graphs_root: Path) -> GraphBuildReport:
    nodes_path, edges_path, state_path, delta_dir = _graph_root_files(graphs_root)
    state = load_graph_state(state_path)
    first_run = not nodes_path.exists() or not edges_path.exists() or not state_path.exists()

    raw_records = discover_concept_records(concepts_root)
    grouped = _group_records_by_key(raw_records)
    merged_records = {key: _merge_records(records) for key, records in grouped.items()}
    alias_lookup = _alias_lookup(merged_records)

    node_lookup: dict[str, GraphNode] = {}
    current_nodes: list[GraphNode] = []
    for key in sorted(merged_records):
        record = merged_records[key]
        node = _build_node(record)
        current_nodes.append(node)
        node_lookup[key] = node

    edge_specs = _build_edge_specs(merged_records, node_lookup, alias_lookup)
    current_edges = _merge_edges(edge_specs, node_lookup)

    current_node_fingerprints = {node.node_id: stable_fingerprint(node.__dict__) for node in current_nodes}
    current_edge_fingerprints = {edge.edge_id: stable_fingerprint(edge.__dict__) for edge in current_edges}

    report = GraphBuildReport(concepts_processed=len(current_nodes))

    previous_node_ids = set(state.node_fingerprints)
    previous_edge_ids = set(state.edge_fingerprints)
    current_node_ids = set(current_node_fingerprints)
    current_edge_ids = set(current_edge_fingerprints)

    for node in current_nodes:
        fingerprint = current_node_fingerprints[node.node_id]
        previous = state.node_fingerprints.get(node.node_id)
        if previous is None:
            report.nodes_created.append(node.node_id)
        elif previous != fingerprint:
            report.nodes_updated.append(node.node_id)
        else:
            report.nodes_unchanged.append(node.node_id)

    for node_id in sorted(previous_node_ids - current_node_ids):
        report.nodes_deleted.append(node_id)

    for edge in current_edges:
        fingerprint = current_edge_fingerprints[edge.edge_id]
        previous = state.edge_fingerprints.get(edge.edge_id)
        if previous is None:
            report.edges_created.append(edge.edge_id)
        elif previous != fingerprint:
            report.edges_updated.append(edge.edge_id)
        else:
            report.edges_unchanged.append(edge.edge_id)
    for edge_id in sorted(previous_edge_ids - current_edge_ids):
        report.edges_deleted.append(edge_id)

    current_state = GraphState(
        schema_version=state.schema_version or 1,
        generated_at=datetime.now(timezone.utc).isoformat(),
        node_fingerprints=current_node_fingerprints,
        edge_fingerprints=current_edge_fingerprints,
        concept_node_ids={key: node.node_id for key, node in node_lookup.items()},
    )

    nodes_dirty = first_run or current_node_fingerprints != state.node_fingerprints or current_node_ids != previous_node_ids
    edges_dirty = first_run or current_edge_fingerprints != state.edge_fingerprints or current_edge_ids != previous_edge_ids

    if nodes_dirty:
        save_graph_nodes(nodes_path, current_nodes)
    if edges_dirty:
        save_graph_edges(edges_path, current_edges)
    if nodes_dirty or edges_dirty:
        save_graph_state(state_path, current_state)
        delta_dir.mkdir(parents=True, exist_ok=True)
        delta_path = delta_dir / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
        delta_path.write_text(
            json.dumps(
                {
                    "generated_at": current_state.generated_at,
                    "nodes_created": report.nodes_created,
                    "nodes_updated": report.nodes_updated,
                    "nodes_deleted": report.nodes_deleted,
                    "edges_created": report.edges_created,
                    "edges_updated": report.edges_updated,
                    "edges_deleted": report.edges_deleted,
                    "unresolved_edge_targets": report.unresolved_edge_targets,
                },
                indent=2,
                ensure_ascii=True,
                sort_keys=True,
            ),
            encoding="utf-8",
        )

    return report
