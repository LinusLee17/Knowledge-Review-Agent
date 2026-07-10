# PDF skill integration

## Status

This repo does not install a local PDF parsing stack.
In this environment, the Anthropic PDF skill is not exposed as an importable Python module or package.
Skill 1 therefore calls the installed Anthropic PDF skill through an external bridge command.

## Foundation

Use the Anthropic PDF skill for layout-aware PDF handling.
The bridge command must emit JSON with this shape:

```json
{
  "title": "string",
  "page_count": 1,
  "warnings": ["string"],
  "pages": [
    {
      "page_number": 1,
      "heading": "string",
      "extracted_text": "string",
      "tables": [],
      "image_count": 0,
      "concept_candidates": ["string"]
    }
  ]
}
```

The extractor only normalizes that payload and writes Markdown + provenance.
The incremental ingest layer then stores lecture artifacts in `data/processed/` and updates `data/index.json`.

## Runtime note

`ANTHROPIC_PDF_SKILL_COMMAND` is required.
The command can be a wrapper script around the installed PDF skill.
There is no supported direct Python API in this checkout, so the bridge is the correct integration point.

## Outside Codex

If this repo runs elsewhere, install:

- the installed Anthropic PDF skill
- a bridge command that emits the JSON contract above

Then point `ANTHROPIC_PDF_SKILL_COMMAND` at that bridge.
