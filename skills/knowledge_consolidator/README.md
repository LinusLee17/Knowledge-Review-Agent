# Knowledge Consolidator

## Purpose

Transform lecture-level concept candidates into canonical study pages organized around learning flow.

## Flow

1. Evidence collection
2. Evidence synthesis
3. Knowledge enrichment
4. Study-flow rendering

## Evidence Collection

Responsibilities:

- merge duplicate concepts
- collect provenance
- aggregate examples and equations
- preserve source lecture files and page references

## Evidence Synthesis

Responsibilities:

- synthesize coherent definitions
- rewrite fragmented lecture notes into durable knowledge
- combine multiple lecture explanations
- remove redundancy

## Knowledge Enrichment

Responsibilities:

- supplement missing intuition with well-established background knowledge
- improve educational value without changing lecture meaning
- add practical applications
- add assumptions and limitations
- add interview questions and common mistakes
- surface graph-like connections in prose

## Study-Flow Rendering

Canonical pages should read like revision guides, not internal logs.

Recommended order:

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

## Inputs

- extracted Markdown notes
- concept candidates
- provenance records

## Outputs

- canonical concept page per concept
- provenance list for each canonical page
- merged explanation text
- draft output only, before evaluation and presentation refinement

## Rules

- Lecture material remains the primary source.
- Supplement only with well-established knowledge.
- Never contradict lecture content.
- Clearly distinguish slide-derived content from enriched content.
- Preserve provenance.
- Keep study pages concise, specific, and interview oriented.
- Keep pipeline metadata at the bottom of the page.

## Notes

- detect duplicates across courses
- remove redundancy
- keep original source references
- route ambiguous merges to review
- do not polish presentation
