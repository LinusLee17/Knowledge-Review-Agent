---
concept_name: "Functional Dependency"
canonical_key: "functional dependency"
concept_type: "theory"
domain: "Data Science"
topic: "Database Design"
importance_score: 4
scope_level: 4
study_priority: 4
version_number: 2
last_updated_timestamp: "2026-07-14T17:35:38.268683+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Functional Dependency

## Classification
- domain: Data Science
- topic: Database Design
- type: theory
- scope: 4/5 (topic or workflow)
- study priority: 4/5
- broader topic(s): Data Management

## Contributing Courses
- BT2102

## Definition
A functional dependency states that one set of attributes determines another set of attributes in a relation. It helps identify keys, validate schemas, and reason about redundancy during database design.

## Why it Matters
Functional Dependency provides a formal way to support Data Integrity, Schema Design under stated assumptions.

## Core Intuition
If knowing X always tells you Y, then X determines Y; that dependency is a clue about how the schema should be designed.

## How it Works
1. Identify a determinant attribute set X and a dependent set Y.
2. Check whether each valid X value determines one Y value.
3. Use the dependency to reason about keys, redundancy, and normalization.

## Key Components
- Determinant X
- Dependent attributes Y
- Candidate keys
- Inference rules
- Schema constraints

## Common Mistakes
- Assuming a dependency from a sample that does not hold as a business rule.
- Confusing a functional dependency with a correlation.
- Using dependencies without checking the determinant and candidate keys.

## Real-world Applications
- Data Integrity
- Schema Design

## Interview Questions
- What problem does Functional Dependency solve, and what is its output?
- Explain Functional Dependency using one concrete input-to-decision example.
- What assumptions must hold before using Functional Dependency?
- Which trade-off decides whether to use Functional Dependency instead of an alternative?
- How does Functional Dependency compare with Database Normalization?

## Related Concepts
- Database Normalization
- Primary Key

## Connections
- Depends on: Relational Data Model
- Used in: Schema Design and Data Integrity
- Related: Database Normalization and Primary Key
- Broader topic: Data Management and Database Design

## Prerequisites
- Relational Data Model

## Slide-derived Evidence
- BT2102 | p10 | [BT2102-06-FunctionalDependency.pdf](../data/raw/BT2102/BT2102-06-FunctionalDependency.pdf#page=10) — Functional Dependency The determinant of a functional dependency refers to the attribute Example: Functional Dependency

## Provenance
- BT2102 | p10 | [BT2102-06-FunctionalDependency.pdf](../data/raw/BT2102/BT2102-06-FunctionalDependency.pdf#page=10) — Functional Dependency The determinant of a functional dependency refers to the attribute Example: Functional Dependency

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.813
- evidence strength: 0.8
- definition quality: 0.74
- interview relevance: 0.94
- version: 2
- last updated: 2026-07-14T17:35:38.268683+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- no meaningful equation or formal relationship extracted
- assumptions not extracted
- trade-offs or limitations not extracted
