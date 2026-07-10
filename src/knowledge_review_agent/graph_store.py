from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import TypeVar

from .models import GraphEdge, GraphNode, GraphState

T = TypeVar("T")


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True), encoding="utf-8")


def stable_fingerprint(payload: object) -> str:
    encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def load_graph_state(state_path: Path) -> GraphState:
    payload = _read_json(state_path)
    return GraphState(
        schema_version=int(payload.get("schema_version", 1) or 1),
        generated_at=str(payload.get("generated_at", "") or ""),
        node_fingerprints=dict(payload.get("node_fingerprints", {}) or {}),
        edge_fingerprints=dict(payload.get("edge_fingerprints", {}) or {}),
        concept_node_ids=dict(payload.get("concept_node_ids", {}) or {}),
    )


def save_graph_state(state_path: Path, state: GraphState) -> None:
    state.generated_at = datetime.now(timezone.utc).isoformat()
    _write_json(state_path, asdict(state))


def load_graph_nodes(nodes_path: Path) -> list[GraphNode]:
    payload = _read_json(nodes_path)
    nodes = payload.get("nodes", []) or []
    return [GraphNode(**node) for node in nodes]


def save_graph_nodes(nodes_path: Path, nodes: list[GraphNode]) -> None:
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nodes": [asdict(node) for node in nodes],
    }
    _write_json(nodes_path, payload)


def load_graph_edges(edges_path: Path) -> list[GraphEdge]:
    payload = _read_json(edges_path)
    edges = payload.get("edges", []) or []
    return [GraphEdge(**edge) for edge in edges]


def save_graph_edges(edges_path: Path, edges: list[GraphEdge]) -> None:
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "edges": [asdict(edge) for edge in edges],
    }
    _write_json(edges_path, payload)
