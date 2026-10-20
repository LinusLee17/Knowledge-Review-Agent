#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from dataclasses import replace, asdict
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from knowledge_review_agent.concept_quality import (  # noqa: E402
    DEFAULT_EXCLUDED_COURSES,
    audit_definition,
    select_source_evidence,
    repair_definition,
    repair_page_sections,
)

from knowledge_review_agent.source_occurrences import load_source_index  # noqa: E402

from knowledge_review_agent.concept_store import (  # noqa: E402
    load_concept_metadata, recover_concept_transactions, write_concept_record,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit and repair concept definitions from processed lecture JSON.")
    parser.add_argument("--processed", default=str(ROOT / "data" / "processed"))
    parser.add_argument("--concepts", default=str(ROOT / "knowledge_base" / "concepts"))
    parser.add_argument("--report", default=str(ROOT / "evaluation" / "runs" / "concept_quality_audit.json"))
    parser.add_argument("--apply", action="store_true", help="write repairs; default only audits")
    return parser.parse_args()


def _validate_repair_root(concepts: Path) -> None:
    root = concepts.resolve()
    published = (ROOT / "knowledge_base" / "refined").resolve()
    if (any(path.name.casefold() == "refined" for path in (root, *root.parents))
            or root.is_relative_to(published) or published.is_relative_to(root)
            or (root / "refined").exists()):
        raise ValueError("Repair requires a draft root separate from published refined directories")


def main() -> int:
    args = parse_args()
    processed = Path(args.processed)
    concepts = Path(args.concepts)
    report_path = Path(args.report)
    forbidden = (concepts, processed, concepts.parent / "refined", ROOT / "knowledge_base" / "refined")
    if any(report_path.resolve().is_relative_to(root.resolve()) for root in forbidden):
        raise ValueError("Audit report must be outside draft/source/refined roots")
    if args.apply:
        _validate_repair_root(concepts)
        # Recovery may retire or replace records, so enumerate only afterward.
        recover_concept_transactions(concepts)
    index = load_source_index(processed)
    findings = []
    repaired = []
    for metadata_path in sorted(concepts.glob("*/metadata.json")):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        courses = set(metadata.get("contributing_courses", []))
        allowed = courses - set(DEFAULT_EXCLUDED_COURSES)
        if not allowed:
            continue
        concept_dir = metadata_path.parent
        concept_md = concept_dir / "concept.md"
        if not concept_md.exists():
            continue
        markdown = concept_md.read_text(encoding="utf-8")
        aliases = [*list(metadata.get("aliases", []) or []), metadata.get("canonical_key", "")]
        scope = {p: metadata.get("source_lecture_hashes", {}).get(p, "")
                 for p in metadata.get("contributing_lecture_files", [])}
        selection = select_source_evidence(index, metadata["concept_name"], aliases, allowed, lecture_hashes=scope)
        support = index.find(metadata["concept_name"], aliases, lecture_hashes=scope, allowed_courses=allowed)
        supported = {o.source.relative_path for o in support.occurrences}
        blocked = [i.code + ": " + i.lecture_file for i in selection.issues]
        blocked.extend("No explicit page support: " + p for p in scope if p not in supported)
        if not selection.coverage:
            blocked.append("No usable source text evidence")
        evidence = list(selection.evidence)
        finding = audit_definition(metadata["concept_name"], metadata, markdown, evidence)
        finding_payload = {**finding.to_dict(), **selection.to_dict(), "repair_blocked": blocked}
        findings.append(finding_payload)
        section_preview, section_repairs = repair_page_sections(metadata["concept_name"], metadata, markdown)
        needs_repair = finding.action == "repair" or bool(section_repairs)
        if not args.apply or not needs_repair or blocked:
            continue
        if finding.action == "repair":
            updated, replacement = repair_definition(metadata["concept_name"], metadata, markdown, evidence)
        else:
            updated, replacement = markdown, metadata.get("definition", "")
        updated, _ = repair_page_sections(metadata["concept_name"], metadata, updated)
        stored = load_concept_metadata(metadata_path)
        candidate = replace(stored, definition=replacement or stored.definition,
                            definition_quality_score=max(stored.definition_quality_score, 0.75))

        def render(final):
            text = updated
            if text.startswith("---\n") and "\n---" in text[4:]:
                boundary = text.index("\n---", 4)
                header, rest = text[:boundary], text[boundary:]
                header = re.sub(r"(?m)^version_number:.*$", f"version_number: {final.version_number}", header)
                header = re.sub(r"(?m)^last_updated_timestamp:.*$", f'last_updated_timestamp: "{final.last_updated_timestamp}"', header)
                text = header + rest
            return text

        result = write_concept_record(concepts, concept_dir, candidate, render, reason="source-backed draft quality repair")
        if result.changed:
            repaired.append(metadata["concept_name"])

    report = {"source_issues": [asdict(i) for i in index.issues], "excluded_courses": sorted(DEFAULT_EXCLUDED_COURSES), "apply": args.apply, "findings": findings, "repaired": repaired}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"eligible": len(findings), "flagged": sum(1 for item in findings if item["action"] == "repair"), "repaired": repaired, "report": report_path.as_posix()}, indent=2))
    return 1 if any(f["repair_blocked"] for f in findings) else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        raise SystemExit(1)
