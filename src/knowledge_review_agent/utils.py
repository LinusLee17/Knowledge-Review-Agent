from __future__ import annotations

import re
from pathlib import Path


_STOP_PHRASES = {
    "agenda",
    "example",
    "examples",
    "introduction",
    "lecture",
    "notes",
    "overview",
    "page",
    "presentation",
    "schedule",
    "slide",
    "summary",
    "table of contents",
}

_CONCEPT_ARTICLES = {"a", "an", "the"}
_CONCEPT_STOP_TOKENS = {"and", "or", "of", "to", "for", "in", "on", "at", "with", "by"}


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def normalize_spaces(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = normalize_spaces(raw)
        if line:
            lines.append(line)
    return lines


def normalize_concept(text: str) -> str:
    text = normalize_spaces(text)
    text = text.strip(" \t-:;,.")
    text = re.sub(r"^[0-9]+[.)]\s*", "", text)
    return text


def singularize_token(token: str) -> str:
    token = normalize_spaces(token).lower()
    if len(token) <= 3:
        return token
    if token.endswith(("ss", "us", "is", "ics", "ias")):
        return token
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"
    if token.endswith(("sses", "shes", "ches", "xes", "zes", "ses")) and len(token) > 4:
        return token[:-2]
    if token.endswith("s") and len(token) > 4:
        return token[:-1]
    return token


def normalize_concept_key(text: str) -> str:
    text = normalize_concept(text).lower()
    text = text.replace("&", " and ")
    text = text.replace("-", " ")
    text = re.sub(r"[()\[\]{}.,;:!?/\\]+", " ", text)
    tokens: list[str] = []
    for token in text.split():
        if token in _CONCEPT_ARTICLES:
            continue
        if token in _CONCEPT_STOP_TOKENS:
            tokens.append(token)
            continue
        tokens.append(singularize_token(token))
    return normalize_spaces(" ".join(tokens))


def canonical_concept_name(text: str) -> str:
    key = normalize_concept_key(text)
    if not key:
        return ""
    return " ".join(part.upper() if len(part) <= 3 and part.isalpha() else part.capitalize() for part in key.split())


def is_candidate_concept(text: str) -> bool:
    cleaned = normalize_concept(text)
    if not cleaned:
        return False
    lowered = cleaned.lower()
    if lowered in _STOP_PHRASES:
        return False
    if len(cleaned) < 3 or len(cleaned) > 120:
        return False
    word_count = len(cleaned.split())
    if word_count < 1 or word_count > 8:
        return False
    if not re.search(r"[A-Za-z]", cleaned):
        return False
    return True


def markdown_escape_cell(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    return text.replace("|", "\\|").replace("\n", " ").strip()


def truncate(text: str, limit: int = 160) -> str:
    text = normalize_spaces(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"
