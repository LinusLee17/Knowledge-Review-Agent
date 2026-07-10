from __future__ import annotations

import json
from pathlib import Path

from knowledge_review_agent.ingestion import run_incremental_ingestion
from knowledge_review_agent.models import PageExtraction
from knowledge_review_agent.pdf_skill_adapter import PdfSkillResult, StaticPdfSkillBridge
from knowledge_review_agent.slide_extractor import run_slide_extractor


class CountingBridge:
    def __init__(self) -> None:
        self.calls: list[Path] = []

    def extract(self, pdf_path: Path) -> PdfSkillResult:
        self.calls.append(pdf_path)
        stem = pdf_path.stem
        return PdfSkillResult(
            title=stem,
            page_count=1,
            warnings=[],
            pages=[
                PageExtraction(
                    page_number=1,
                    heading=stem.replace("_", " ").title(),
                    extracted_text=f"{stem}\nConcept A\nConcept B",
                    tables=[],
                    image_count=0,
                    concept_candidates=[stem.replace("_", " ").title()],
                )
            ],
        )


def test_slide_extractor_writes_lecture_markdown_and_json(tmp_path: Path) -> None:
    raw_root = tmp_path / "data" / "raw"
    processed_root = tmp_path / "data" / "processed"
    raw_root.mkdir(parents=True)
    processed_root.mkdir(parents=True)

    metadata_csv = tmp_path / "data" / "metadata.csv"
    metadata_csv.parent.mkdir(parents=True, exist_ok=True)
    metadata_csv.write_text(
        "course_id,course_name,category,semester,folder,notes\n"
        "ds101,Data Science 101,statistics,2025S,data/raw,\n",
        encoding="utf-8",
    )

    pdf_path = raw_root / "lecture1.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%stub\n")

    bridge = StaticPdfSkillBridge(
        PdfSkillResult(
            title="Linear Regression",
            page_count=2,
            warnings=[],
            pages=[
                PageExtraction(
                    page_number=1,
                    heading="Linear Regression",
                    extracted_text=(
                        "Linear Regression\n"
                        "Linear Regression is a statistical method that estimates the relationship between a target and one or more predictors by fitting a linear function.\n"
                        "y = b + mx\n"
                        "Assumptions: linearity, independence, constant variance.\n"
                        "Used for prediction, forecasting, and interpreting variable effects."
                    ),
                    tables=[],
                    image_count=0,
                    concept_candidates=["Linear Regression"],
                ),
                PageExtraction(
                    page_number=2,
                    heading="Assumptions",
                    extracted_text="Linearity\nIndependence\nHomoscedasticity",
                    tables=[],
                    image_count=0,
                    concept_candidates=["Assumptions"],
                ),
            ],
        )
    )

    results = run_slide_extractor(
        raw_root=raw_root,
        processed_root=processed_root,
        metadata_csv=metadata_csv,
        skill_bridge=bridge,
        pdf_paths=[pdf_path],
    )

    assert len(results) == 1
    lecture_md = Path(results[0]["lecture_md"])
    lecture_json = Path(results[0]["lecture_json"])
    lecture_dir = Path(results[0]["lecture_dir"])

    assert lecture_md.exists()
    assert lecture_json.exists()
    assert lecture_dir.exists()

    lecture_text = lecture_md.read_text(encoding="utf-8")
    lecture_json_text = lecture_json.read_text(encoding="utf-8")

    assert "Data Science 101" in lecture_text
    assert "## Page 1: Linear Regression" in lecture_text
    assert "Linear Regression is a statistical method" in lecture_text
    assert '"concept_candidates"' in lecture_json_text
    assert "Assumptions" in lecture_json_text


def test_slide_extractor_filters_slide_noise_and_emits_metrics(tmp_path: Path) -> None:
    raw_root = tmp_path / "data" / "raw"
    processed_root = tmp_path / "data" / "processed"
    raw_root.mkdir(parents=True)
    processed_root.mkdir(parents=True)

    metadata_csv = tmp_path / "data" / "metadata.csv"
    metadata_csv.parent.mkdir(parents=True, exist_ok=True)
    metadata_csv.write_text(
        "course_id,course_name,category,semester,folder,notes\n"
        "ds101,Data Science 101,statistics,2025S,data/raw,\n",
        encoding="utf-8",
    )

    pdf_path = raw_root / "lecture2.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%stub\n")

    bridge = StaticPdfSkillBridge(
        PdfSkillResult(
            title="Agenda",
            page_count=1,
            warnings=[],
            pages=[
                PageExtraction(
                    page_number=1,
                    heading="Agenda",
                    extracted_text=(
                        "PCA is used to reduce dimensionality by projecting data onto directions of maximum variance.\n"
                        "It helps with visualization, compression, and noise reduction in high-dimensional datasets.\n"
                        "This is useful when the original feature space is large and correlated."
                    ),
                    tables=[],
                    image_count=0,
                    concept_candidates=["PCA"],
                )
            ],
        )
    )

    results = run_slide_extractor(
        raw_root=raw_root,
        processed_root=processed_root,
        metadata_csv=metadata_csv,
        skill_bridge=bridge,
        pdf_paths=[pdf_path],
    )

    lecture_json = Path(results[0]["lecture_json"])
    payload = json.loads(lecture_json.read_text(encoding="utf-8"))
    page = payload["pages"][0]

    assert payload["metrics"]["total_pages_processed"] == 1
    assert payload["metrics"]["candidate_concepts_generated"] >= 1
    assert payload["metrics"]["concepts_accepted"] == 0
    assert payload["metrics"]["rejected_low_depth"] >= 1
    assert page["concepts"] == []
    assert [item["concept_name"] for item in page["candidate_concepts"]] == ["PCA"]
    assert "Agenda" not in page["concept_candidates"]
    assert "Week 5" not in page["concept_candidates"]


def test_slide_extractor_rejects_template_like_profile_pages(tmp_path: Path) -> None:
    raw_root = tmp_path / "data" / "raw"
    processed_root = tmp_path / "data" / "processed"
    raw_root.mkdir(parents=True)
    processed_root.mkdir(parents=True)

    metadata_csv = tmp_path / "data" / "metadata.csv"
    metadata_csv.parent.mkdir(parents=True, exist_ok=True)
    metadata_csv.write_text(
        "course_id,course_name,category,semester,folder,notes\n"
        "ds101,Data Science 101,statistics,2025S,data/raw,\n",
        encoding="utf-8",
    )

    pdf_path = raw_root / "lecture3.pdf"
    pdf_path.write_bytes(b"%PDF-1.4\n%stub\n")

    bridge = StaticPdfSkillBridge(
        PdfSkillResult(
            title="PCA",
            page_count=1,
            warnings=[],
            pages=[
                PageExtraction(
                    page_number=1,
                    heading="PCA",
                    extracted_text=(
                        "PCA\n"
                        "PCA is used for visualization and compression.\n"
                        "Dimensionality Reduction.\n"
                        "Noise Reduction."
                    ),
                    tables=[],
                    image_count=0,
                    concept_candidates=["PCA"],
                )
            ],
        )
    )

    results = run_slide_extractor(
        raw_root=raw_root,
        processed_root=processed_root,
        metadata_csv=metadata_csv,
        skill_bridge=bridge,
        pdf_paths=[pdf_path],
    )

    lecture_json = Path(results[0]["lecture_json"])
    payload = json.loads(lecture_json.read_text(encoding="utf-8"))
    page = payload["pages"][0]

    assert payload["metrics"]["candidate_concepts_generated"] >= 1
    assert payload["metrics"]["concepts_accepted"] == 0
    assert payload["metrics"]["rejected_low_depth"] >= 1
    assert page["concepts"] == []


def test_incremental_ingestion_skips_unchanged_hashes(tmp_path: Path) -> None:
    raw_root = tmp_path / "data" / "raw"
    processed_root = tmp_path / "data" / "processed"
    raw_root.mkdir(parents=True)
    processed_root.mkdir(parents=True)

    metadata_csv = tmp_path / "data" / "metadata.csv"
    metadata_csv.parent.mkdir(parents=True, exist_ok=True)
    metadata_csv.write_text(
        "course_id,course_name,category,semester,folder,notes\n"
        "ds101,Data Science 101,statistics,2025S,data/raw,\n",
        encoding="utf-8",
    )

    index_path = tmp_path / "data" / "index.json"
    bridge = CountingBridge()

    pdf1 = raw_root / "lecture1.pdf"
    pdf2 = raw_root / "lecture2.pdf"
    pdf1.write_bytes(b"alpha")
    pdf2.write_bytes(b"beta")

    first = run_incremental_ingestion(
        raw_root=raw_root,
        processed_root=processed_root,
        index_path=index_path,
        metadata_csv=metadata_csv,
        skill_bridge=bridge,
    )
    assert len(first.processed) == 2
    assert len(bridge.calls) == 2
    assert index_path.exists()

    second_bridge = CountingBridge()
    second = run_incremental_ingestion(
        raw_root=raw_root,
        processed_root=processed_root,
        index_path=index_path,
        metadata_csv=metadata_csv,
        skill_bridge=second_bridge,
    )
    assert len(second.processed) == 0
    assert len(second.skipped) == 2
    assert len(second_bridge.calls) == 0

    pdf2.write_bytes(b"beta-updated")
    third_bridge = CountingBridge()
    third = run_incremental_ingestion(
        raw_root=raw_root,
        processed_root=processed_root,
        index_path=index_path,
        metadata_csv=metadata_csv,
        skill_bridge=third_bridge,
    )
    assert len(third_bridge.calls) == 1
    assert len(third.processed) == 1
    assert index_path.exists()
