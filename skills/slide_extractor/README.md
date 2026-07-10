# Slide Extractor

## Purpose

Transform parsed lecture content into high-quality candidate knowledge concepts.

## Inputs

- source PDF in `data/raw/`
- course metadata from `data/metadata.csv`

## Outputs

- Markdown notes
- source attribution
- concept candidates
- structured extraction artifacts

## Foundation

The Slide Extractor is designed to run inside Codex.

It relies on the installed Anthropic PDF Skill for all PDF parsing and layout-aware document inspection.

The Slide Extractor must not implement its own PDF parser.

Whenever PDF parsing is required, invoke the installed Anthropic PDF Skill through Codex's Skill system rather than using standalone Python libraries.

## Responsibilities

Identify durable concepts.
Reject slide noise.
Assign domains and topics.
Estimate confidence.
Preserve provenance.
Produce structured concept candidates.

## Acceptance criteria

"A concept should only be accepted if it represents durable knowledge that deserves its own revision page."

A concept must pass all of these checks:

1. Is it a meaningful standalone idea?
2. Does it have a clear definition?
3. Would a data science student revise this concept later?
4. Does it have technical depth, practical relevance, or interview value?
5. Is it more than a generic word?

If any answer is no, reject or merge it into a broader concept.

Do not accept based only on:

* appearing once
* appearing in a heading
* appearing in a bullet point
* appearing as a table label

## Notes

- Reject headings, agenda items, OCR artifacts.
- Reject generic terms unless sufficiently contextualized.
- keep page-level provenance
- mark uncertain text instead of guessing
- ignore course related information such as lecturer backgrounds, assignment deadlines, grading rubrics, and other non-conceptual information
