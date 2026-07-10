from __future__ import annotations

import json
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

from .models import CourseMetadata, DocumentExtraction, PageExtraction
from .utils import normalize_lines

PARSER_VERSION = "anthropic-pdf-skill-bridge/1"


@dataclass(frozen=True)
class PdfSkillResult:
    title: str
    page_count: int
    pages: list[PageExtraction]
    warnings: list[str]


@runtime_checkable
class PdfSkillBridge(Protocol):
    def extract(self, pdf_path: Path) -> PdfSkillResult:
        raise NotImplementedError


class ExternalPdfSkillBridge:
    """Invoke installed Anthropic PDF skill through configured command."""

    def __init__(self, command: str | None = None) -> None:
        self.command = command or os.environ.get("ANTHROPIC_PDF_SKILL_COMMAND", "").strip()

    def extract(self, pdf_path: Path) -> PdfSkillResult:
        command = self.command
        if not command:
            raise RuntimeError(
                "ANTHROPIC_PDF_SKILL_COMMAND not set. Configure it to a wrapper that "
                "invokes the installed Anthropic PDF skill and emits JSON."
            )

        args = shlex.split(command) + [str(pdf_path)]
        completed = subprocess.run(args, check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RuntimeError(
                "PDF skill command failed "
                f"exit={completed.returncode} stderr={completed.stderr.strip()}"
            )

        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("PDF skill command must emit JSON to stdout") from exc

        return self.from_payload(payload)

    @staticmethod
    def from_payload(payload: dict) -> PdfSkillResult:
        pages_payload = payload.get("pages", [])
        pages: list[PageExtraction] = []
        for item in pages_payload:
            extracted_text = item.get("extracted_text", "")
            if isinstance(extracted_text, list):
                extracted_text = "\n".join(str(line) for line in extracted_text)
            extracted_text = "\n".join(normalize_lines(str(extracted_text)))

            pages.append(
                PageExtraction(
                    page_number=int(item.get("page_number", len(pages) + 1)),
                    heading=str(item.get("heading", "") or ""),
                    extracted_text=extracted_text,
                    tables=item.get("tables", []) or [],
                    image_count=int(item.get("image_count", 0) or 0),
                    concept_candidates=[
                        str(value).strip()
                        for value in (item.get("concept_candidates", []) or [])
                        if str(value).strip()
                    ],
                )
            )

        return PdfSkillResult(
            title=str(payload.get("title", "") or ""),
            page_count=int(payload.get("page_count", len(pages)) or len(pages)),
            pages=pages,
            warnings=[
                str(value).strip()
                for value in (payload.get("warnings", []) or [])
                if str(value).strip()
            ],
        )


class StaticPdfSkillBridge:
    def __init__(self, result: PdfSkillResult) -> None:
        self.result = result

    def extract(self, pdf_path: Path) -> PdfSkillResult:  # noqa: ARG002
        return self.result


def result_to_document_extraction(
    pdf_path: Path,
    relative_path: Path,
    course: CourseMetadata,
    result: PdfSkillResult,
) -> DocumentExtraction:
    return DocumentExtraction(
        pdf_path=pdf_path,
        relative_path=relative_path,
        course=course,
        title=result.title or course.course_name or pdf_path.stem,
        page_count=result.page_count or len(result.pages),
        pages=result.pages,
        warnings=list(result.warnings),
    )
