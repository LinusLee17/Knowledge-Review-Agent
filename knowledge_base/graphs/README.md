# Knowledge Graph Builder

Incremental knowledge-graph data lives here.

## Explain:
- node normalization
- alias resolution
- prerequisite relationships
- related concepts
- scope level and study priority
- broader topics and applications remain concept metadata, not graph edges

Visible relationship types:

- `prerequisite`: directed learning dependency
- `related`: undirected conceptual association

`scope_level` describes structural breadth (5 = broad family, 1 = narrow detail).
`study_priority` describes learner value. They are separate dimensions; scope controls node size, while priority remains available for future filtering.

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
