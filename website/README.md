# Website

Generated interactive knowledge site lives here.

Source inputs:

- `knowledge_base/refined/**/concept.md`
- `knowledge_base/refined/**/metadata.json`
- `knowledge_base/graphs/graph.json`

Rules:

- render refined knowledge only
- preserve navigation and provenance
- do not re-extract or re-consolidate knowledge
- keep presentation separate from knowledge generation

The graph view is a thin Cytoscape.js presentation layer. It reads the graph bundle directly and does not rebuild relationships in the browser.

Browser loads graph.json only; nodes.json/edges.json are internal diagnostics,
not fallback inputs. graph-contract.mjs validates complete schema 1/2 before graph
initialization and blocks unsafe concept paths before Markdown fetch. Failure
shows useful error instead of guessing missing data.

Custom deployments can set data-graph-url, data-refined-root-url and
data-repo-root-url on index.html document root. Set matching published/repo roots
on concept.html. Defaults match conventional repository layout; no runtime config
fetch or build step. Python export must use matching explicit roots. Existing
Cytoscape/MathJax CDN runtime dependencies remain unchanged.

Concept pages use `concept-markdown.mjs` for the supported Markdown subset:
sections, introductory prose, fenced code, equations, tables, inline links and
images. Asset URLs resolve relative to the fetched Markdown; legacy source-PDF
URLs in the checked-in pages retain their repository-root targets. Source PDFs
remain local-only. The renderer does not claim full CommonMark support.
