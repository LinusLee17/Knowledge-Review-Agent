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
