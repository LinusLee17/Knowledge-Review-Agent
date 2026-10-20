from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from collections.abc import Mapping
from .source_occurrences import SourceIndex, SourceOccurrence, SourceIssue, SourceValidationError, load_source_index
from pathlib import Path

from .utils import normalize_concept_key, normalize_spaces


DEFAULT_EXCLUDED_COURSES = frozenset({"Auto-ML", "IS3103", "BT2101", "BT3102", "BT2102"})


@dataclass(frozen=True)
class SourceEvidence:
    course_id: str
    lecture_file: str
    page_number: int
    text: str
    occurrences: tuple[SourceOccurrence, ...] = ()


@dataclass(frozen=True)
class QualityFinding:
    concept_name: str
    courses: list[str]
    score: float
    flags: list[str]
    definition: str
    evidence: list[SourceEvidence]
    action: str

    def to_dict(self) -> dict[str, object]:
        return {"concept_name": self.concept_name, "courses": self.courses, "score": self.score,
                "flags": self.flags, "definition": self.definition, "action": self.action,
                "evidence": [_evidence_payload(e) for e in self.evidence]}


def _sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "__preamble__"
    for line in markdown.splitlines():
        match = re.match(r"^##\s+(.*)$", line)
        if match:
            current = normalize_spaces(match.group(1))
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def _definition(markdown: str) -> str:
    return normalize_spaces(_sections(markdown).get("Definition", ""))


def _clean_source_line(value: str) -> str:
    text = normalize_spaces(value)
    text = re.sub(r"^[•▪◦o\-]+\s*", "", text)
    text = re.sub(r"\(cid:\d+\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    return normalize_spaces(text)


def _is_source_candidate(text: str, concept_name: str, aliases: list[str]) -> bool:
    lowered = text.lower()
    if len(text.split()) < 8 or len(text.split()) > 70:
        return False
    if "?" in text or lowered.startswith(("recall:", "example:", "agenda", "summary", "page ", "slide ")):
        return False
    if any(token in lowered for token in ("topic02-", "nus cs", "lecture ", "copyright", "all rights reserved")):
        return False
    normalized = normalize_concept_key(text)
    canonical = normalize_concept_key(concept_name)
    # Short aliases (H0, CLT, PCA) create false matches in slide residue.
    # Prefer full canonical-name evidence; aliases remain useful only when
    # canonical name is absent from source wording.
    if canonical and canonical in normalized:
        return True
    names = [normalize_concept_key(alias) for alias in aliases if len(normalize_concept_key(alias)) >= 4]
    return any(name and name in normalized for name in names)


def _reference(o: SourceOccurrence) -> dict:
    return {"occurrence_id": o.occurrence_id, "lecture_file": o.source.relative_path,
            "lecture_sha256": o.source.sha256, "course": o.source.course, "source_pdf": o.source.source_pdf,
            "page_number": o.page_number, "json_pointer": o.json_pointer, "line_number": o.line_number,
            "start": o.start, "end": o.end, "text": o.text}


def _evidence_payload(e: SourceEvidence) -> dict:
    return {"course_id": e.course_id, "lecture_file": e.lecture_file, "page_number": e.page_number,
            "text": e.text, "occurrences": [_reference(o) for o in e.occurrences]}


@dataclass(frozen=True)
class SourceEvidenceSelection:
    evidence: tuple[SourceEvidence, ...]
    coverage: tuple[SourceOccurrence, ...]
    issues: tuple[SourceIssue, ...]

    def to_dict(self) -> dict:
        return {"source_coverage": [_reference(o) for o in self.coverage],
                "source_issues": [asdict(i) for i in self.issues]}


def select_source_evidence(index: SourceIndex, concept_name: str, aliases: list[str],
                           allowed_courses: set[str], limit: int = 8, *,
                           lecture_hashes: Mapping[str, str] | None = None) -> SourceEvidenceSelection:
    if limit < 0:
        raise ValueError("Evidence limit must be nonnegative")
    matches = index.find(concept_name, aliases, lecture_hashes=lecture_hashes,
                         allowed_courses=allowed_courses, kinds=("text_line",), text_search=True)
    candidates = []
    for occurrence in matches.occurrences:
        text = _clean_source_line(occurrence.text)
        if not _is_source_candidate(text, concept_name, aliases):
            continue
        lowered = text.lower()
        score = 0.0
        if re.search(r"\b(is|are|occurs|measures|describes|represents|called|refers to|defined as)\b", lowered): score += 3.0
        if lowered.startswith(tuple(alias.lower() for alias in [concept_name, *aliases] if alias.strip())): score += 2.0
        if any(token in lowered for token in ("when", "used to", "distribution", "probability", "error", "generalize", "uncertainty")): score += 1.0
        score += 1.0 if text.endswith((".", '."', "?", "!")) else -1.0
        if text.endswith(("is", "of", "because", "then", "as", "to", "in")): score -= 3.0
        candidates.append((score, text, occurrence))
    candidates.sort(key=lambda c: (-c[0], len(c[1]), c[2].source.relative_path, c[2].page_number,
                                   c[2].json_pointer, c[2].line_number))
    grouped = {}
    for _, text, occurrence in candidates:
        grouped.setdefault(text.lower(), []).append((text, occurrence))
    evidence = []
    for values in list(grouped.values())[:limit]:
        text, first = values[0]
        evidence.append(SourceEvidence(first.source.course, first.source.relative_path, first.page_number,
                                       text, tuple(o for _, o in values)))
    coverage = tuple(sorted((o for _, _, o in candidates),
        key=lambda o: (o.source.relative_path, o.page_number, o.json_pointer, o.line_number)))
    return SourceEvidenceSelection(tuple(evidence), coverage, matches.issues)


def collect_source_evidence(processed_root: Path, concept_name: str, aliases: list[str],
                            allowed_courses: set[str], limit: int = 8, *,
                            source_index: SourceIndex | None = None,
                            lecture_hashes: Mapping[str, str] | None = None) -> list[SourceEvidence]:
    selection = select_source_evidence(source_index if source_index is not None else load_source_index(processed_root),
        concept_name, aliases, allowed_courses, limit, lecture_hashes=lecture_hashes)
    if selection.issues:
        raise SourceValidationError(selection.issues)
    return list(selection.evidence)


def audit_definition(concept_name: str, metadata: dict, markdown: str, evidence: list[SourceEvidence]) -> QualityFinding:
    definition = _definition(markdown)
    lowered = definition.lower()
    flags: list[str] = []
    if not definition:
        flags.append("missing_definition")
    if len(definition.split()) < 18:
        flags.append("definition_too_short")
    if not lowered.startswith(concept_name.lower()):
        flags.append("does_not_identify_concept_first")
    if normalize_concept_key(concept_name) in {"decision tree", "decision trees"} and lowered.startswith(concept_name.lower() + " is "):
        flags.append("subject_verb_mismatch")
    if any(token in lowered for token in ("(cid:", "recall:", "example:", "one--sample", "simple linear regression", "lecture ")):
        flags.append("slide_or_ocr_residue")
    if any(token in lowered for token in ("durable building block", "surrounding topic", "what is overfitting", "durable idea worth remembering")):
        flags.append("boilerplate")
    if definition.endswith(("is", "of", "because", "then", "as", "to", "from", "in")):
        flags.append("incomplete_sentence")
    if definition.count("|") > 1 or definition.count("  ") > 2:
        flags.append("format_residue")
    sections = _sections(markdown)
    for section_name, markers, flag in (
        ("Why it Matters", ("explicit concept and evidence trail", "durable building block", "reusable building block", "provides a formal way to support"), "generic_why_it_matters"),
        ("Core Intuition", ("durable building block", "language that makes the rest", "mental model: use stated assumptions", "mental model: transform inputs", "how knowing the sampling"), "generic_intuition"),
        ("How it Works", ("identify object and intended question", "apply definition under its assumptions", "start from the inputs", "specify inputs and objective", "count the relevant outcomes", "define the objects and events precisely"), "generic_workflow"),
        ("Key Components", ("prerequisites:", "decision/use context:", "neighbor concepts:", "core definitions", "- assumptions\n", "- implications\n"), "generic_components"),
        ("Common Mistakes", ("do not memorize", "nearby but different concept"), "generic_mistakes"),
    ):
        content = sections.get(section_name, "").lower()
        if any(marker in content for marker in markers):
            flags.append(flag)
    score = max(0.0, 1.0 - 0.12 * len(flags))
    action = "repair" if flags else "keep"
    courses = sorted(set(metadata.get("contributing_courses", [])))
    return QualityFinding(concept_name, courses, round(score, 3), flags, definition, evidence, action)


def _replace_section(markdown: str, section_name: str, replacement: str) -> str:
    return re.sub(
        rf"(^##\s+{re.escape(section_name)}\n)(.*?)(?=\n##\s+|\Z)",
        lambda match: match.group(1) + replacement.rstrip() + "\n",
        markdown,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )


def section_repairs(concept_name: str, metadata: dict, markdown: str) -> dict[str, str]:
    sections = _sections(markdown)
    name_key = normalize_concept_key(concept_name)
    concept_type = str(metadata.get("concept_type", "concept") or "concept").lower()
    applications = [str(item) for item in metadata.get("applications", []) if str(item).strip()]
    related = [str(item) for item in metadata.get("related_concepts", []) if str(item).strip()]
    repairs: dict[str, str] = {}
    why = sections.get("Why it Matters", "").lower()
    if any(marker in why for marker in ("explicit concept and evidence trail", "durable building block", "reusable building block", "provides a formal way to support", "makes ", "under stated assumptions")):
        if name_key == "overfitting":
            repairs["Why it Matters"] = "It matters because a model can look successful on training data while failing on unseen cases. Detecting and controlling this gap protects generalization and makes validation results trustworthy."
        elif concept_type == "metric":
            repairs["Why it Matters"] = f"It matters because it makes {', '.join(applications[:3]) or 'model or data behavior'} measurable, enabling explicit comparisons and decisions."
        elif concept_type in {"error", "concept"} and "error" in name_key:
            repairs["Why it Matters"] = "It matters because it connects a statistical decision with its possible failure mode, allowing error probabilities and consequences to be discussed explicitly."
        else:
            repairs["Why it Matters"] = f"It matters because it provides a concrete way to reason about {', '.join(applications[:3]) or metadata.get('topic') or 'the surrounding problem'} and choose an appropriate next action."
    intuition = sections.get("Core Intuition", "").lower()
    if any(marker in intuition for marker in ("durable building block", "language that makes the rest", "mental model: use stated assumptions", "mental model: transform inputs", "how knowing the sampling", "summary number")):
        if name_key == "overfitting":
            repairs["Core Intuition"] = "A model has learned details of its training sample instead of the stable pattern. Training error keeps falling while validation or test error stops improving or rises."
        elif name_key in {"p value", "test statistic", "null hypothesis", "alternative hypothesis", "type i error", "type ii error"}:
            repairs["Core Intuition"] = "Think of a hypothesis test as a controlled comparison: state a baseline, measure how far observed data move from it, then account for uncertainty before deciding."
        elif "distribution" in name_key:
            repairs["Core Intuition"] = "Imagine repeating the same sampling process many times. The statistic changes from sample to sample; its distribution describes that variation and therefore the uncertainty of one observed estimate."
        elif concept_type == "metric":
            repairs["Core Intuition"] = "A metric compresses several observed outcomes into one number. Meaning comes from what it counts, what it divides by, and which error or decision it emphasizes."
        else:
            repairs["Core Intuition"] = "Understand the concept as a link between inputs, assumptions, and an observable output. Change one assumption at a time and check how the result changes."
    how = sections.get("How it Works", "").lower()
    if any(marker in how for marker in ("identify object and intended question", "apply definition under its assumptions", "start from the inputs", "specify inputs and objective", "count the relevant outcomes", "define the objects and events precisely")):
        if name_key == "overfitting":
            repairs["How it Works"] = "1. Split data into training and validation/test sets without leakage.\n2. Fit models of increasing flexibility or complexity.\n3. Compare training error with validation/test error.\n4. If the gap grows, reduce complexity, regularize, collect more data, or improve validation."
        elif concept_type == "metric":
            repairs["How it Works"] = "1. Define the target quantity and population.\n2. Identify the observed outcomes and denominator.\n3. Compute the metric.\n4. Interpret its scale with uncertainty, class balance, and decision cost."
        elif "hypothesis" in name_key or "error" in name_key or name_key in {"p value", "test statistic"}:
            repairs["How it Works"] = "1. State null and alternative claims.\n2. Choose a test statistic and its null distribution.\n3. Compute the statistic and p-value or critical-region decision.\n4. Report the decision, uncertainty, effect size, and possible error."
        elif "distribution" in name_key or concept_type in {"theory", "theorem"}:
            repairs["How it Works"] = "1. Define the random quantity and sampling process.\n2. State conditions and parameters.\n3. Derive or approximate the distribution or result.\n4. Use it to quantify uncertainty and check whether conditions fit the data."
        else:
            repairs["How it Works"] = "1. Define the question, inputs, and assumptions.\n2. Apply the method or relationship.\n3. Produce the estimate, prediction, or decision.\n4. Evaluate the result against an explicit criterion and known limitations."
    components = sections.get("Key Components", "").lower()
    if any(marker in components for marker in ("prerequisites:", "decision/use context:", "neighbor concepts:", "core definitions", "- assumptions\n", "- implications\n")):
        if concept_type == "metric":
            repairs["Key Components"] = "- Quantity being measured\n- Numerator and denominator\n- Scale and uncertainty\n- Decision cost or error trade-off"
        elif "hypothesis" in name_key or "error" in name_key or name_key in {"p value", "test statistic"}:
            repairs["Key Components"] = "- Null and alternative hypotheses\n- Test statistic and null distribution\n- Significance level or decision threshold\n- Effect size and Type I/II error consequences"
        elif "distribution" in name_key:
            repairs["Key Components"] = "- Random quantity or statistic\n- Sampling process\n- Probability law or approximation\n- Parameters and uncertainty interpretation"
        else:
            repairs["Key Components"] = "- Inputs and objective\n- Core transformation or rule\n- Output and evaluation criterion\n- Assumptions and failure modes"
    mistakes = sections.get("Common Mistakes", "").lower()
    if any(marker in mistakes for marker in ("do not memorize", "nearby but different concept")):
        repairs["Common Mistakes"] = "- Applying the concept without checking its assumptions or data context.\n- Reporting a result without explaining what it measures and what it cannot establish.\n- Confusing the concept with a related quantity, method, or decision rule."
    return repairs


def repair_page_sections(concept_name: str, metadata: dict, markdown: str) -> tuple[str, dict[str, str]]:
    repairs = section_repairs(concept_name, metadata, markdown)
    updated = markdown
    for section_name, replacement in repairs.items():
        updated = _replace_section(updated, section_name, replacement)
    return updated, repairs


def _generic_definition(concept_name: str, metadata: dict, evidence: list[SourceEvidence]) -> str:
    concept_type = str(metadata.get("concept_type", "concept") or "concept").lower()
    domain = str(metadata.get("domain", "") or "").strip()
    topic = str(metadata.get("topic", "") or "").strip()
    applications = [str(item) for item in metadata.get("applications", []) if str(item).strip()]
    context = f" in {domain}" if domain else ""
    focus = f" for {topic}" if topic else ""
    name_key = normalize_concept_key(concept_name)
    specific_keys = {
        "precision", "recall", "margin of error", "confidence interval", "standard error",
        "test statistic", "sampling distribution", "central limit theorem", "hypothesis testing",
        "null hypothesis", "alternative hypothesis", "type i error", "type ii error", "p value",
        "decision tree", "decision trees", "random forest", "pca", "regularization", "overfitting",
    }
    if name_key == "precision":
        first = "Precision is the fraction of predicted positive cases that are actually positive: TP/(TP+FP). It penalizes false positives."
    elif name_key == "recall":
        first = "Recall is the fraction of actual positive cases that are identified: TP/(TP+FN). It penalizes false negatives."
    elif name_key == "margin of error":
        first = "Margin of Error is the half-width that quantifies sampling uncertainty around a point estimate, commonly computed as a critical value multiplied by a standard error."
    elif name_key == "confidence interval":
        first = "Confidence Interval is an interval-estimation procedure that produces a range of plausible parameter values together with a stated confidence level."
    elif name_key == "standard error":
        first = "Standard Error measures the sampling variability of an estimator; smaller standard error means the estimator varies less across repeated samples."
    elif name_key == "test statistic":
        first = "Test Statistic is a quantity computed from sample data and compared with a null distribution to assess a hypothesis."
    elif name_key == "sampling distribution":
        first = "Sampling Distribution is the probability distribution of a statistic across repeated samples from a population or data-generating process."
    elif name_key == "central limit theorem":
        first = "Central Limit Theorem states that, under suitable conditions, the standardized sum or sample mean approaches a normal distribution as sample size grows."
    elif name_key == "hypothesis testing":
        first = "Hypothesis Testing is a procedure that compares sample evidence with a null hypothesis using a test statistic and decision rule."
    elif name_key == "null hypothesis":
        first = "Null Hypothesis is the baseline statement about a population parameter that a statistical test evaluates for possible rejection."
    elif name_key == "alternative hypothesis":
        first = "Alternative Hypothesis is the statement about a population parameter supported when evidence is inconsistent with the null hypothesis."
    elif name_key == "type i error":
        first = "Type I Error occurs when a test rejects a true null hypothesis; its probability is the significance level α."
    elif name_key == "type ii error":
        first = "Type II Error occurs when a test fails to reject a false null hypothesis; its probability is commonly denoted β."
    elif name_key == "p value":
        first = "p-value is the probability, assuming the null hypothesis is true, of observing a test statistic at least as extreme as the observed value."
    elif name_key in {"decision tree", "decision trees"}:
        first = "Decision Trees are supervised-learning models that recursively split observations by feature rules until terminal leaves support predictions or decisions."
    elif name_key == "random forest":
        first = "Random Forest is an ensemble that combines predictions from many randomized decision trees to reduce variance and improve generalization."
    elif name_key == "pca":
        first = "PCA (Principal Component Analysis) projects data onto orthogonal components ordered by explained variance, reducing dimensions while retaining prominent structure."
    elif name_key == "regularization":
        first = "Regularization controls model complexity by adding a penalty or constraint that discourages unstable parameter values and improves generalization."
    elif name_key == "overfitting":
        first = "Overfitting occurs when a model fits noise or idiosyncrasies in observed training data, giving low training error but poor performance on unseen data."
    elif concept_type == "metric":
        first = f"{concept_name} is a metric that measures a defined aspect of {topic or domain or 'observed data'}."
    elif concept_type == "model":
        first = f"{concept_name} is a model used to estimate, predict, or explain a relationship in {topic or domain or 'data'}."
    elif concept_type in {"algorithm", "method"}:
        first = f"{concept_name} is a systematic procedure for transforming inputs into an output or decision in {topic or domain or 'an analysis task'}."
    elif concept_type == "workflow":
        first = f"{concept_name} is an ordered process for investigating evidence and choosing next actions in {topic or domain or 'an analysis task'}."
    elif concept_type == "theory":
        first = f"{concept_name} is a formal account that connects assumptions, objects, and implications in {topic or domain or 'its field'}."
    elif concept_type == "theorem":
        first = f"{concept_name} is a formally established result that follows under stated assumptions in {topic or domain or 'its field'}."
    elif concept_type == "distribution" or "distribution" in concept_name.lower():
        first = f"{concept_name} is a probability description of how a random quantity or statistic behaves across repeated outcomes."
    elif concept_type == "phenomenon":
        first = f"{concept_name} is a model behavior in which fitting observed data can fail to generalize to unseen data."
    elif "error" in concept_name.lower():
        first = f"{concept_name} is a hypothesis-testing outcome in which a decision conflicts with the true state."
    elif "hypothesis" in concept_name.lower():
        first = f"{concept_name} is a statement about a population parameter or data-generating claim tested against evidence."
    elif "p-value" in concept_name.lower() or "p value" in concept_name.lower():
        first = f"{concept_name} is a probability, calculated under a null hypothesis, of observing a result at least as extreme as the one obtained."
    else:
        first = f"{concept_name} is an idea used to describe, analyze, or make decisions about {topic or domain or 'data and evidence'}."
    trusted_evidence = [] if name_key in specific_keys else [item for item in evidence if _trusted_evidence(concept_name, item.text)]
    if trusted_evidence:
        source_text = trusted_evidence[0].text
        if source_text.lower().startswith(concept_name.lower()):
            source_text = concept_name + source_text[len(concept_name):]
            first = source_text if source_text.endswith(".") else source_text + "."
        elif len(source_text.split()) >= 10:
            first += f" Lecture evidence characterizes it as: {source_text.rstrip('.')} ."
    if applications:
        subject = "They are" if name_key in {"decision tree", "decision trees"} else "It is"
        first += f" {subject} used in {', '.join(applications[:3])}."
    related = [str(item) for item in metadata.get("related_concepts", []) if str(item).strip()]
    if related and concept_type in {"phenomenon", "metric", "method", "algorithm", "model"}:
        first += f" It is commonly considered alongside {', '.join(related[:3])}."
    return normalize_spaces(first.replace(" .", "."))


def _trusted_evidence(concept_name: str, text: str) -> bool:
    normalized = normalize_concept_key(text)
    canonical = normalize_concept_key(concept_name)
    lowered = text.lower()
    if not canonical or canonical not in normalized:
        return False
    concept_start = lowered.startswith(concept_name.lower()) or lowered.startswith((
        f"a {concept_name.lower()}",
        f"an {concept_name.lower()}",
        f"the {concept_name.lower()}",
    ))
    if not concept_start:
        return False
    if text.endswith(("is", "of", "because", "then", "as", "to", "in")):
        return False
    if any(token in lowered for token in ("recall:", "agenda", "schedule", "page ", "lecture ", "topic02-")):
        return False
    if not re.search(r"\b(is a|are|occurs|measures|describes|represents|called|refers to|defined as|phenomenon)\b", lowered):
        return False
    return text.endswith((".", "?", "!")) or len(text.split()) >= 20


def repair_definition(concept_name: str, metadata: dict, markdown: str, evidence: list[SourceEvidence]) -> tuple[str, str]:
    replacement = _generic_definition(concept_name, metadata, evidence)
    updated = re.sub(
        r"(^##\s+Definition\n)(.*?)(?=\n##\s+|\Z)",
        lambda match: match.group(1) + replacement + "\n",
        markdown,
        count=1,
        flags=re.MULTILINE | re.DOTALL,
    )
    return updated, replacement
