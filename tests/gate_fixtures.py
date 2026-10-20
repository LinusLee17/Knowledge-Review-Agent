from dataclasses import replace
from hashlib import sha256
import json
from pathlib import Path

from knowledge_review_agent.concept_store import save_concept_metadata
from knowledge_review_agent.models import ConceptMetadata


DEFINITION = "Linear Regression is a statistical model that estimates a linear relationship between inputs and a numeric response."


def corpus(tmp_path):
    from knowledge_review_agent.quality_gate import GatePaths
    concepts, processed, reviews = (tmp_path / name for name in ("concepts", "processed", "reviews"))
    directory = concepts / "Linear Regression"
    directory.mkdir(parents=True)
    lecture = processed / "C1" / "L1" / "lecture.json"
    lecture.parent.mkdir(parents=True)
    lecture.write_text(json.dumps({"pdf": "C1/L1.pdf", "page_count": 1, "course": {"course_id": "C1"},
        "pages": [{"page_number": 1, "extracted_text": DEFINITION,
                   "concepts": [{"canonical_key": "linear regression", "concept_name": "Linear Regression"}]}]}))
    metadata = ConceptMetadata(concept_name="Linear Regression", canonical_key="linear regression",
        domain="Statistics", topic="Regression", definition=DEFINITION, importance_score=5,
        contributing_courses=["C1"], contributing_lecture_files=["C1/L1/lecture.json"],
        source_lecture_hashes={"C1/L1/lecture.json": sha256(lecture.read_bytes()).hexdigest()})
    save_concept_metadata(directory / "metadata.json", metadata)
    (directory / "concept.md").write_text(f"# Linear Regression\n\n## Definition\n{DEFINITION}\n\n## Provenance\nC1, L1, page 1.\n")
    return GatePaths(concepts, processed, reviews), directory, lecture


def edit_metadata(directory, **values):
    path = directory / "metadata.json"
    payload = json.loads(path.read_text())
    payload.update(values)
    path.write_text(json.dumps(payload))


def inventory(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def review(paths, report, *, disposition="accepted_with_evidence", concept_index=0):
    from knowledge_review_agent.quality_gate import content_digest
    concept = report["concepts"][concept_index]
    findings = [f for f in report["findings"] if f["concept_key"] == concept["concept_key"] and f["severity"] == "review"]
    payload = {"schema_version": 1, "reviewer": "Synthetic test reviewer", "reviewed_at": "2026-10-19T00:00:00Z",
        "rationale": "Synthetic test-only decision with source-page evidence.", "concept_key": concept["concept_key"],
        "concept_fingerprint": concept["fingerprint"], "resolutions": [{"finding_id": f["finding_id"],
        "finding_digest": content_digest(f["details"]), "disposition": disposition,
        "citations": [{"lecture_file": "C1/L1/lecture.json", "page_number": 1}]} for f in findings]}
    payload["record_id"] = content_digest(payload)
    paths.reviews_root.mkdir(parents=True, exist_ok=True)
    path = paths.reviews_root / f"{payload['record_id']}.json"
    path.write_text(json.dumps(payload))
    return path, payload


def approved_report(paths, root):
    from knowledge_review_agent.quality_gate import evaluate_for_refinement, write_evaluation_report
    result = evaluate_for_refinement(paths)
    assert result["eligibility"] == "pass", result["findings"]
    return write_evaluation_report(result, root / "reports")
