# Knowledge Graph Builder

Incremental knowledge-graph data lives here.

## Explain:
- node normalization
- alias resolution
- prerequisite relationships
- related concepts
- broader topics
- application links

Expected layout:

```text
knowledge_base/graphs/
  nodes.json
  edges.json
  graph.json
  state.json
  deltas/
```

Rules:

- update only affected nodes and edges
- keep graph data separate from presentation
- preserve stable node identifiers for future visualization
- keep unresolved targets explicit instead of inventing nodes
- derive graph inputs from refined concept pages
- write `graph.json` as a presentation bundle for the website after graph build
