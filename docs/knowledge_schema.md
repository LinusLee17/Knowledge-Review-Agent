# Knowledge Schema

## Purpose

Canonical concept pages are study guides, not pipeline records. The page should read in the same order a student thinks while revising.

## Canonical Order

1. Title
2. Classification
3. Contributing Courses
4. Definition
5. Why it Matters
6. Core Intuition
7. How it Works
8. Mathematical Foundation
9. Key Components
10. Advantages
11. Limitations
12. Common Mistakes
13. Common Variants
14. Real-world Applications
15. Interview Questions
16. Related Concepts
17. Connections
18. Prerequisites
19. Further Reading
20. Slide-derived Evidence
21. Provenance
22. Extraction Metadata
23. Quality Review (only when evidence is incomplete)

## Section Rules

- `Classification` should hold domain, topic, concept type, importance, aliases, and broader topics.
- `Contributing Courses` should list source courses that contributed evidence.
- `Why it Matters` should answer why the student should remember this concept.
- `Core Intuition` should give the memorable mental model.
- `How it Works` should describe the mechanism or process in steps.
- `Mathematical Foundation` should use a clean display equation when math is real and complete.
- `Key Components` should name the parts a student needs to recall.
- `Common Variants` should list named variants or subtypes, not simple aliases.
- `Common Mistakes` should highlight misconceptions or failure modes.
- `Connections` should express graph-like relations in prose, such as `Depends on`, `Used in`, or `Related`.
- `Interview Questions` should be actual questions a student can practice.
- `Quality Review` must expose missing evidence; it must never be replaced with invented detail.
- `Slide-derived Evidence`, `Provenance`, and `Extraction Metadata` belong at the bottom.

## Definition Quality Requirements

Every accepted concept must have a useful definition. A valid definition should explain:

- what it is
- what problem it solves
- why it matters

Example:

Linear Regression is a statistical modelling method that estimates the relationship between a dependent variable and one or more independent variables by fitting a linear function. It is commonly used for prediction, inference, and understanding variable relationships.

## Mathematical Field Improvements

Do not generate artificial mathematics.

Rules:

- Only populate mathematical foundations when the equation is meaningful.
- Use complete notation and explain the symbols.
- Leave the field empty if the math is incomplete or low value.

## Generic Quality Layer

Concept enrichment must use semantic fields, not one template per concept name:

- choose language from concept type (`workflow`, `metric`, `model`, `method`, etc.)
- compose definition from type + domain/topic + observed purpose/applications
- derive workflow steps from available prerequisites, assumptions, outputs, and evaluation cues
- derive trade-offs and interview prompts from applications, limitations, alternatives, and relations
- emit `Quality Review` when required evidence is missing

Named concept rules are optional overrides. Placeholder overrides must be rejected. Source evidence and graph relations remain authoritative.

Example:

```text
Gradient Descent

\theta_{t+1} = \theta_t - \alpha \nabla J(\theta_t)

| Symbol | Meaning |
| --- | --- |
| \theta_t | Current parameters |
| \alpha | Learning rate |
| \nabla J(\theta_t) | Gradient of the loss |
```

## Application Field Improvements

Applications should represent real-world usage.

Reject:

- Used in examples
- Used in this lecture

Accept:

- Fraud detection
- Customer churn prediction
- Demand forecasting
- Medical diagnosis

## Concept Naming

Concept names should represent durable knowledge units.

Before:

- Accuracy

After:

- Classification Accuracy

Before:

- Regression

After:

- Linear Regression
- Logistic Regression

Avoid overly broad concepts when a more specific canonical name is available.

## Persistence conflicts

Canonical metadata optionally contains `persistence_conflicts` (default `[]` for
legacy records). Each conflict records `field_name`, `selected_value`, and an
`alternatives` list. Each alternative records:

- `source_record`: original concept directory, relative to concepts root.
- `record_sha256`: SHA-256 of original metadata bytes.
- `value`: exact alternative text or lecture hash.
- `snapshot_id`: immutable snapshot path relative to the sibling history root.

`persistence_snapshot_id` optionally records the current write's original
snapshot path (default empty for legacy/new records without previous bytes).
The renderer uses it to rebase local evidence links to archived files. This is
storage provenance, not a technical content claim. Metadata-only helpers do not
allocate snapshots.

For a lecture-hash conflict, `field_name` is
`source_lecture_hashes.<lecture-reference>`. Duplicate primary ordering remains
highest version, latest timestamp, then descending directory path. Preferred
nonempty scalar values stay active; lists union without deleting distinct
contributions. Explicit numeric values remain primary values.

Unresolved alternatives appear under `Quality Review`, with original-record
identity, metadata hash, and archive-manifest reference. Different equations are
not concatenated into an invented mathematical statement. Prior content remains
available in exact original snapshots. Active `Retained Source Material` blocks
keep earlier source evidence and custom sections with attribution, deduplicated
by section name and exact content hash.

Unmatched technical sections in original Markdown also remain visible as
attributed source material. Definitions, intuition, and equations absent from
metadata can be copied literally from their original page sections. Competing
values retain original-record references and review flags; no equation is guessed.

Store-generated versions and timestamps describe committed content changes.
New records start at version 1; updates and duplicate merges advance once from
the maximum contributing version. No-op runs and recovery do not advance them.

## Source occurrence identity

Occurrences are derived in memory from lecture JSON, not stored as a second
canonical metadata database. Source kinds are `structured`, `candidate` and
`text_line`. Each location retains course, lecture-relative path, exact lecture
SHA-256, PDF path, positive page number and JSON pointer. Text lines additionally
retain 1-based line number and zero-based character offsets excluding newline.
Raw wording/spacing remains exact; cleaned display wording is separate.

Occurrence IDs hash source policy `1`, lecture-relative path/hash and locator
using deterministic canonical JSON. Changed lecture bytes create new IDs. Equal
wording on different pages/lectures retains distinct IDs. Existing canonical
metadata needs no new field, version bump or implicit rewrite.

Audit `source_coverage` lists all accepted text occurrences before display cap;
each displayed evidence group's `occurrences` lists every citation for that
wording. Source presence alone does not verify a definition or approve a merge.
