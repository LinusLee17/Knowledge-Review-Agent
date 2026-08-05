from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .concept_store import load_concept_metadata
from .models import GraphEdge, GraphNode
from .utils import normalize_concept_key, normalize_spaces


@dataclass(frozen=True)
class GraphBundleNode:
    node_id: str
    concept_key: str
    concept_name: str
    domain: str
    topic: str
    importance_score: int
    scope_level: int
    study_priority: int
    contributing_courses: list[str]
    contributing_lecture_files: list[str]
    aliases: list[str]
    prerequisites: list[str]
    related_concepts: list[str]
    broader_topics: list[str]
    applications: list[str]
    definition: str
    core_idea: str
    interview_notes: str
    connected_edge_count: int
    degree: int
    metadata_path: str
    metadata_url: str
    concept_url: str
    search_terms: list[str]


@dataclass(frozen=True)
class GraphBundleEdge:
    edge_id: str
    source: str
    target: str
    relation_type: str
    source_concept_key: str
    target_concept_key: str
    source_concept_name: str
    target_concept_name: str
    target_resolved: bool
    supporting_courses: list[str]
    supporting_lecture_files: list[str]
    supporting_lecture_hashes: dict[str, str]


@dataclass
class GraphBundle:
    generated_at: str
    schema_version: int = 1
    stats: dict[str, object] = field(default_factory=dict)
    nodes: list[GraphBundleNode] = field(default_factory=list)
    edges: list[GraphBundleEdge] = field(default_factory=list)


def _repo_root(graphs_root: Path) -> Path:
    return graphs_root.parent.parent.resolve()


def _relative_site_path(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def _site_url(repo_root: Path, path: Path) -> str:
    relative = _relative_site_path(repo_root, path)
    return f"../{relative}"


def _concept_viewer_url(repo_root: Path, path: Path) -> str:
    relative = _relative_site_path(repo_root, path).replace("metadata.json", "concept.md")
    relative = relative.replace("knowledge_base/concepts/", "knowledge_base/refined/", 1)
    return f"./concept.html?path=../{relative}"


def _parse_markdown_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = defaultdict(list)
    current = "__preamble__"
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = normalize_spaces(line[3:])
            continue
        if line.startswith("# ") and current == "__preamble__":
            continue
        sections[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def _safe_read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _unique_text_list(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = normalize_spaces(str(value or ""))
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(text)
    return result


def _extract_support_text(sections: dict[str, str], *names: str) -> str:
    for name in names:
        content = sections.get(name, "").strip()
        if content:
            return content
    return ""


def _load_node_bundle(node: GraphNode, graphs_root: Path) -> dict[str, object]:
    repo_root = _repo_root(graphs_root)
    metadata_path = Path(node.metadata_path)
    metadata = load_concept_metadata(metadata_path)
    concept_md_path = metadata_path.with_name("concept.md")
    concept_md = _safe_read_text(concept_md_path)
    sections = _parse_markdown_sections(concept_md)

    definition = normalize_spaces(metadata.definition if metadata else "")
    intuition = normalize_spaces(metadata.intuition if metadata else "")
    applications = _unique_text_list(list(metadata.applications) if metadata else [])
    prerequisites = _unique_text_list(list(metadata.prerequisites) if metadata else [])
    related_concepts = _unique_text_list(list(metadata.related_concepts) if metadata else [])
    broader_topics = _unique_text_list(list(metadata.broader_topics) if metadata else [])
    aliases = _unique_text_list(list(metadata.aliases) if metadata else [])
    if metadata and metadata.concept_name and metadata.concept_name not in aliases:
        aliases = [*aliases, metadata.concept_name]

    interview_notes = _extract_support_text(
        sections,
        "Interview Questions",
        "Common Mistakes",
    )
    core_idea = _extract_support_text(
        sections,
        "Core Intuition",
        "Why it Matters",
    )
    if not core_idea:
        core_idea = intuition or definition

    search_terms = _unique_text_list(
        [
            node.concept_name,
            node.concept_key,
            node.domain,
            node.topic,
            *(metadata.contributing_courses if metadata else []),
            *aliases,
            *prerequisites,
            *related_concepts,
            *broader_topics,
            *applications,
        ]
    )

    return {
        "node_id": node.node_id,
        "concept_key": node.concept_key,
        "concept_name": node.concept_name,
        "domain": node.domain,
        "topic": node.topic,
        "importance_score": node.importance_score,
        "scope_level": node.scope_level,
        "study_priority": node.study_priority,
        "contributing_courses": sorted(set(node.contributing_courses)),
        "contributing_lecture_files": sorted(set(node.contributing_lecture_files)),
        "aliases": aliases,
        "prerequisites": prerequisites,
        "related_concepts": related_concepts,
        "broader_topics": broader_topics,
        "applications": applications,
        "definition": definition,
        "core_idea": core_idea,
        "interview_notes": interview_notes,
        "connected_edge_count": 0,
        "degree": 0,
        "metadata_path": _relative_site_path(repo_root, metadata_path),
        "metadata_url": _site_url(repo_root, metadata_path),
        "concept_url": _concept_viewer_url(repo_root, metadata_path),
        "search_terms": search_terms,
    }


def _load_edge_bundle(edge: GraphEdge) -> dict[str, object]:
    return {
        "edge_id": edge.edge_id,
        "source": edge.source_node_id,
        "target": edge.target_node_id,
        "relation_type": edge.relation_type,
        "source_concept_key": edge.source_concept_key,
        "target_concept_key": edge.target_concept_key,
        "source_concept_name": edge.source_concept_name,
        "target_concept_name": edge.target_concept_name,
        "target_resolved": edge.target_resolved,
        "supporting_courses": sorted(set(edge.supporting_courses)),
        "supporting_lecture_files": sorted(set(edge.supporting_lecture_files)),
        "supporting_lecture_hashes": dict(sorted(edge.supporting_lecture_hashes.items())),
    }


def build_graph_bundle(nodes: list[GraphNode], edges: list[GraphEdge], graphs_root: Path, generated_at: str) -> GraphBundle:
    node_payloads = [_load_node_bundle(node, graphs_root) for node in nodes]
    edge_payloads = [_load_edge_bundle(edge) for edge in edges]

    degree: dict[str, int] = Counter()
    for edge in edge_payloads:
        source = str(edge["source"])
        target = str(edge["target"])
        degree[source] += 1
        degree[target] += 1

    for node in node_payloads:
        count = degree.get(str(node["node_id"]), 0)
        node["connected_edge_count"] = count
        node["degree"] = count

    domains = sorted({str(node["domain"]) for node in node_payloads if str(node["domain"]).strip()})
    multi_course = sum(1 for node in node_payloads if len(node["contributing_courses"]) > 1)
    avg_degree = round(sum(degree.values()) / len(node_payloads), 2) if node_payloads else 0.0
    relation_counts = Counter(edge["relation_type"] for edge in edge_payloads)

    stats = {
        "total_concepts": len(node_payloads),
        "total_edges": len(edge_payloads),
        "domains": domains,
        "average_node_degree": avg_degree,
        "multi_course_concepts": multi_course,
        "relation_counts": dict(sorted(relation_counts.items())),
    }

    return GraphBundle(
        generated_at=generated_at,
        stats=stats,
        nodes=[GraphBundleNode(**node) for node in node_payloads],
        edges=[GraphBundleEdge(**edge) for edge in edge_payloads],
    )


def write_graph_bundle(graphs_root: Path, nodes: list[GraphNode], edges: list[GraphEdge], generated_at: str) -> Path:
    bundle = build_graph_bundle(nodes=nodes, edges=edges, graphs_root=graphs_root, generated_at=generated_at)
    payload = {
        "schema_version": bundle.schema_version,
        "generated_at": bundle.generated_at,
        "stats": bundle.stats,
        "nodes": [node.__dict__ for node in bundle.nodes],
        "edges": [edge.__dict__ for edge in bundle.edges],
    }
    graph_json = graphs_root / "graph.json"
    graph_json.parent.mkdir(parents=True, exist_ok=True)
    graph_json.write_text(json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True), encoding="utf-8")
    return graph_json
