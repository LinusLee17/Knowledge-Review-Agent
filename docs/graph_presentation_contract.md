# Graph presentation contract

`graph.json` is the browser's only graph data input. Python exports schema 2;
complete schema-1 presentation bundles remain readable via explicit legacy adapter.
Raw internal nodes/edges are not presentation bundles and cannot rescue bad input.

All fields declared by GraphBundleNode and GraphBundleEdge are required. Content
may be empty string/list/map; null or absent values are invalid. Ranks are integers
1..5, counts nonnegative integers, target_resolved boolean true. Node IDs and edge
IDs share one unique namespace; canonical keys are unique opaque identifiers.
Endpoints must exist and keys agree; relations are prerequisite or related; self
edges are invalid. Isolated nodes and empty graphs are valid presentation data.

Stats count actual nodes/edges, distinct course IDs, sorted nonblank domains,
relation counts and incident degree. Average degree uses nonnegative half-up
rounding to two decimals. Domain order uses Unicode code points, never locale.
Timestamp must be calendar-valid timezone-bearing ISO-8601 with seconds and optional
1..6 fractional digits. Validators return normalized copy, preserving prose and
provenance. Unknown extension values must remain finite JSON-compatible values.

V2 metadata_path names repo-relative refined metadata. Metadata URL and viewer
path query must resolve to same refined concept directory. Encode resource path,
then encode that URL as query value. Decode only relevant layer: literal percent
escapes in filenames must not become traversal/separators. Reject external,
absolute, malformed, escaping or conflicting targets. V1 adapter trusts validated
published metadata_url over old draft metadata_path without fetching drafts.

GraphPresentationPaths declares repository, draft, refined and website roots.
Graph output directory never defines site URL meaning. check_files additionally
requires actual refined metadata/Markdown and viewer. Export validates matching
refined version/classification/ranks/contributions before publishing; browser
validation alone cannot verify file contents or factual correctness.

Contract errors expose code/location/message via GraphContractError. Missing or
invalid graph produces error, not inferred topology. Publication is atomic per
file; unchanged semantic payload preserves old bytes/mtime/timestamp. Internal
state/delta transactions remain independent. Single-writer operation only.
Publication preserves existing file permissions; new graph.json uses mode 0644.
Output symlinks inside repository are rejected before any builder writes; system
aliases above declared roots remain allowed.
