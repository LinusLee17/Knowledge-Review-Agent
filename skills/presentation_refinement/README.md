# Presentation Refinement

## Purpose

Apply Impeccable-backed presentation polish to consolidated concept pages.
The executable stage lives in `scripts/refine_concepts.py`.

## Inputs

- draft concept pages
- evaluation pass/fail status
- provenance records

## Outputs

- refined concept pages in `knowledge_base/refined/`
- presentation-only layout and formatting updates
- unchanged semantic content

## Constraints

- preserve meaning
- preserve citations and provenance
- do not invent knowledge
- do not modify equations or factual claims
- do not perform extraction or reasoning

## Notes

- presentation layer only
- runs after evaluation and quality gate
- output feeds website generation
