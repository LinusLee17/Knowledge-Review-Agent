"""Lossless concept sections and evidence links shared by gate and formatter."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re
from urllib.parse import urlsplit

CANONICAL_SECTION_ORDER = [
    "Classification",
    "Contributing Courses",
    "Definition",
    "Why it Matters",
    "Core Intuition",
    "How it Works",
    "Mathematical Foundation",
    "Key Components",
    "Advantages",
    "Limitations",
    "Common Mistakes",
    "Common Variants",
    "Real-world Applications",
    "Interview Questions",
    "Related Concepts",
    "Connections",
    "Prerequisites",
    "Further Reading",
    "Slide-derived Evidence",
    "Provenance",
    "Extraction Metadata",
]

SECTION_ALIASES = {
    "real-world applications": "Real-world Applications",
    "real world applications": "Real-world Applications",
    "applications": "Real-world Applications",
    "assumptions": "Assumptions",
}


@dataclass(frozen=True)
class DocumentSection:
    heading: str
    content: str


@dataclass(frozen=True)
class ConceptDocument:
    prefix: str
    title: str
    sections: tuple[DocumentSection, ...]


def canonical_section_name(name: str) -> str:
    key = " ".join(name.split()).lower()
    return SECTION_ALIASES.get(key, next((n for n in CANONICAL_SECTION_ORDER if n.lower() == key), name.strip()))


def _lines(markdown: str):
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").splitlines(keepends=True)
    fence = ""
    size = 0
    front = bool(lines and lines[0].strip() == "---")
    for i, line in enumerate(lines):
        if front:
            yield line, False
            if i and line.strip() == "---":
                front = False
            continue
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\n"))
        if fence:
            yield line, False
            if marker and marker[1][0] == fence and len(marker[1]) >= size and not marker[2].strip():
                fence = ""
            continue
        if marker:
            fence, size = marker[1][0], len(marker[1])
            yield line, False
        else:
            yield line, True
    if fence:
        raise ValueError("Unclosed Markdown fence; preservation cannot be proven")
    if front:
        raise ValueError("Unclosed front matter; preservation cannot be proven")


def parse_concept_document(markdown: str) -> ConceptDocument:
    prefix = []
    sections = []
    current = None
    body = []
    title = ""
    for line, visible in _lines(markdown):
        heading = re.match(r"^##[ \t]+(.+?)\s*$", line) if visible else None
        if heading:
            if current is not None:
                sections.append(DocumentSection(current, "".join(body)))
            current, body = heading[1], []
        elif current is None:
            prefix.append(line)
            if visible and line.startswith("# ") and not title:
                title = line[2:].strip()
        else:
            body.append(line)
    if current is not None:
        sections.append(DocumentSection(current, "".join(body)))
    return ConceptDocument("".join(prefix), title, tuple(sections))


def format_concept_document(markdown: str) -> str:
    document = parse_concept_document(markdown)
    order = {name.lower(): i for i, name in enumerate(CANONICAL_SECTION_ORDER)}
    sections = sorted(enumerate(document.sections), key=lambda pair: (
        order.get(canonical_section_name(pair[1].heading).lower(), len(order)), pair[0],
    ))
    result = [document.prefix.rstrip("\n")]
    for _, section in sections:
        result.append(f"## {canonical_section_name(section.heading)}\n{section.content.strip(chr(10))}")
    return "\n\n".join(result).rstrip("\n") + "\n"


def assert_presentation_preserved(original: str, formatted: str) -> None:
    def identity(text):
        document = parse_concept_document(text)
        return document.prefix.rstrip("\n"), Counter(
            (canonical_section_name(s.heading), s.content.strip("\n")) for s in document.sections
        )
    if identity(original) != identity(formatted):
        raise ValueError("Presentation did not preserve concept content")


# Shared tokenization retains labels/titles so rebasing changes destinations only.
REFERENCE_PATTERN = re.compile(r'^( {0,3}\[[^\]\n]+\]:[ \t]*)(.+?)(\n?)$')


def link_destination(raw: str) -> tuple[str, str]:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        end = raw.index(">")
        return raw[1:end], raw[end + 1:]
    suffix = re.search(r"\s+(?:\".*\"|'.*'|\(.*\))$", raw)
    return (raw[:suffix.start()], suffix[0]) if suffix else (raw, "")


def _mapped_destination(raw, transform):
    destination, title = link_destination(raw)
    changed = transform(destination)
    if changed == destination:
        return raw
    if raw.strip().startswith("<"):
        changed = f"<{changed}>"
    return changed + title


def _inline_link_starts(text):
    # Ignore code contents without splitting enclosing labels or changing offsets.
    text = re.sub(r"`+[^`]*`+", lambda match: " " * len(match[0]), text)
    # Balance labels rather than stopping at the first (possibly escaped) bracket.
    brackets = []
    index = 0
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "[":
            brackets.append(index)
        elif char == "]" and brackets:
            start = brackets.pop()
            if text[index + 1:index + 2] == "(":
                yield start, index + 2
        index += 1


def _map_inline_links(text, transform):
    result = []
    offset = 0
    for _, end in _inline_link_starts(text):
        # An outer label can begin before an already mapped inner image/link.
        if end <= offset:
            continue
        depth, quote, angle = 1, "", False
        index = end
        while index < len(text):
            char = text[index]
            if char == "\\":
                index += 2
                continue
            if quote:
                if char == quote:
                    quote = ""
            elif angle:
                if char == ">":
                    angle = False
            elif char == "<":
                angle = True
            elif char in "\"'" and index > end and text[index - 1].isspace():
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if not depth:
                    break
            index += 1
        if depth:
            continue
        result.extend((text[offset:end], _mapped_destination(text[end:index], transform), ")"))
        offset = index + 1
    result.append(text[offset:])
    return "".join(result)


def map_document_links(markdown: str, transform) -> str:
    result = []
    for line, visible in _lines(markdown):
        if not visible:
            result.append(line)
            continue
        reference = REFERENCE_PATTERN.match(line)
        if reference:
            result.append(reference[1] + _mapped_destination(reference[2], transform) + reference[3])
            continue
        result.append(_map_inline_links(line, transform))
    return "".join(result)


def local_document_links(markdown: str) -> tuple[str, ...]:
    links = []
    def collect(destination):
        url = urlsplit(destination)
        if not url.scheme and not url.netloc and url.path:
            links.append(destination)
        return destination
    map_document_links(markdown, collect)
    return tuple(links)
