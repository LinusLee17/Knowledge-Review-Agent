#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


def _clean_text(value: str) -> str:
    text = str(value or "").replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _looks_like_heading(line: str) -> bool:
    text = _clean_text(line)
    if not text:
        return False
    lower = text.lower()
    if "@" in text or re.search(r"\b\d{3,}\b", text):
        return False
    if re.fullmatch(r"[\d/.-]+", text):
        return False
    if lower.startswith(("page ", "slide ", "week ")):
        return False
    words = text.split()
    return 2 <= len(words) <= 14


def _infer_heading(text: str) -> str:
    lines = [_clean_text(line) for line in text.splitlines()]
    candidates = [line for line in lines if _looks_like_heading(line)]
    if candidates:
        candidates.sort(key=lambda value: (len(value), -sum(ch.isupper() for ch in value)), reverse=True)
        return candidates[0][:160]
    for line in lines:
        if line:
            return line[:160]
    return ""


def _extract_tables(page: pdfplumber.page.Page) -> list[list[list[str]]]:
    tables: list[list[list[str]]] = []
    try:
        extracted = page.extract_tables() or []
    except Exception:
        extracted = []
    for table in extracted:
        cleaned_table: list[list[str]] = []
        for row in table or []:
            cleaned_row = [_clean_text(cell) for cell in (row or [])]
            if any(cell for cell in cleaned_row):
                cleaned_table.append(cleaned_row)
        if cleaned_table:
            tables.append(cleaned_table)
    return tables


def _extract_pages(pdf_path: Path) -> dict[str, object]:
    reader = PdfReader(str(pdf_path))
    title = ""
    try:
        metadata = reader.metadata
        if metadata and metadata.title:
            title = _clean_text(metadata.title)
    except Exception:
        title = ""

    pages: list[dict[str, object]] = []
    warnings: list[str] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for index, page in enumerate(pdf.pages, start=1):
            try:
                text = page.extract_text(layout=True) or ""
            except Exception:
                text = ""
                warnings.append(f"page {index}: text extraction failed")
            text = _clean_text(text)
            heading = _infer_heading(text)
            tables = _extract_tables(page)
            image_count = len(getattr(page, "images", []) or [])
            if not text and not tables:
                warnings.append(f"page {index}: empty extraction")
            pages.append(
                {
                    "page_number": index,
                    "heading": heading,
                    "extracted_text": text,
                    "tables": tables,
                    "image_count": image_count,
                    "concept_candidates": [],
                }
            )

    return {
        "title": title or pdf_path.stem,
        "page_count": len(pages),
        "warnings": warnings,
        "pages": pages,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bridge wrapper for Anthropic PDF skill JSON contract.")
    parser.add_argument("pdf_path", help="Input PDF")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        raise SystemExit(f"missing pdf: {pdf_path}")
    payload = _extract_pages(pdf_path)
    print(json.dumps(payload, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
