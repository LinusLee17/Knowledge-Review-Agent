#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from knowledge_review_agent.concept_quality import (  # noqa: E402
    DEFAULT_EXCLUDED_COURSES,
    audit_definition,
    collect_source_evidence,
    repair_definition,
    repair_page_sections,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit and repair concept definitions from processed lecture JSON.")
    parser.add_argument("--processed", default=str(ROOT / "data" / "processed"))
    parser.add_argument("--concepts", default=str(ROOT / "knowledge_base" / "concepts"))
    parser.add_argument("--refined", default=str(ROOT / "knowledge_base" / "refined"))
    parser.add_argument("--report", default=str(ROOT / "evaluation" / "runs" / "concept_quality_audit.json"))
    parser.add_argument("--apply", action="store_true", help="write repairs; default only audits")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    processed = Path(args.processed)
    concepts = Path(args.concepts)
    refined = Path(args.refined)
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
        aliases = list(metadata.get("aliases", []) or [])
        evidence = collect_source_evidence(processed, metadata["concept_name"], aliases, allowed)
        finding = audit_definition(metadata["concept_name"], metadata, markdown, evidence)
        findings.append(finding.to_dict())
        section_preview, section_repairs = repair_page_sections(metadata["concept_name"], metadata, markdown)
        needs_repair = finding.action == "repair" or bool(section_repairs)
        if not args.apply or not needs_repair:
            continue
        if finding.action == "repair":
            updated, replacement = repair_definition(metadata["concept_name"], metadata, markdown, evidence)
        else:
            updated, replacement = markdown, metadata.get("definition", "")
        updated, _ = repair_page_sections(metadata["concept_name"], metadata, updated)
        concept_md.write_text(updated, encoding="utf-8")
        if replacement:
            metadata["definition"] = replacement
        metadata["definition_quality_score"] = max(float(metadata.get("definition_quality_score", 0.0)), 0.75)
        metadata["version_number"] = int(metadata.get("version_number", 1) or 1) + 1
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        refined_md = refined / concept_dir.name / "concept.md"
        if refined_md.exists():
            refined_text = refined_md.read_text(encoding="utf-8")
            if replacement:
                refined_text = re.sub(r"(^##\s+Definition\n)(.*?)(?=\n##\s+|\Z)", lambda m: m.group(1) + replacement + "\n", refined_text, count=1, flags=re.MULTILINE | re.DOTALL)
            refined_text, _ = repair_page_sections(metadata["concept_name"], metadata, refined_text)
            refined_md.write_text(refined_text, encoding="utf-8")
            refined_metadata = refined / concept_dir.name / "metadata.json"
            if refined_metadata.exists():
                refined_payload = json.loads(refined_metadata.read_text(encoding="utf-8"))
                refined_payload.update({"definition": replacement, "definition_quality_score": metadata["definition_quality_score"], "version_number": metadata["version_number"]})
                refined_metadata.write_text(json.dumps(refined_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
        repaired.append(metadata["concept_name"])

    report = {"excluded_courses": sorted(DEFAULT_EXCLUDED_COURSES), "apply": args.apply, "findings": findings, "repaired": repaired}
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"eligible": len(findings), "flagged": sum(1 for item in findings if item["action"] == "repair"), "repaired": repaired, "report": report_path.as_posix()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
