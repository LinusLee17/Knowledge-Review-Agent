---
target: website/index.html
total_score: 25
p0_count: 0
p1_count: 2
timestamp: 2026-07-14T16-21-16Z
slug: website-index-html
---
#### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---:|---|
| 1 | Visibility of System Status | 3 | Filters and graph statistics update, but no compact active-filter summary exists. |
| 2 | Match System / Real World | 3 | Concept, domain, and course language is clear; scope terminology needs explanation. |
| 3 | User Control and Freedom | 3 | Fit and Reset exist, but clearing individual filter groups is slow. |
| 4 | Consistency and Standards | 3 | Controls and panels are consistent; relationship semantics are not explained visually. |
| 5 | Error Prevention | 2 | Filter combinations can hide most of the graph without a strong empty-state recovery path. |
| 6 | Recognition Rather Than Recall | 3 | Domain legend is useful; edge styles lack an equivalent legend. |
| 7 | Flexibility and Efficiency | 3 | Search, layouts, domains, courses, and scope provide strong flexibility. |
| 8 | Aesthetic and Minimalist Design | 2 | The graph becomes visually noisy at full density and sidebars are long. |
| 9 | Error Recovery | 2 | Load failure exposes a generic message without retry guidance. |
| 10 | Help and Documentation | 1 | No concise explanation of node size, edge direction, or relationship styles. |
| **Total** | | **25/40** | Functional MVP with a clear next step: improve graph legibility and orientation. |

#### Anti-Patterns Verdict

**LLM assessment:** The interface does not strongly read as AI-generated. Its restrained palette and product layout fit the study tool. The main generic pattern is a three-column dashboard with a long filter sidebar and a dense central graph.

**Deterministic scan:** Clean. `detect.mjs --json website/index.html` returned no findings.

**Browser evidence:** The page renders at 1280x720 with no horizontal overflow. Graph data loads. Cytoscape logs warnings because `domainColor` is assigned after style initialization; this should be fixed.

#### Overall Impression

The graph is useful as a navigational surface, but the initial view asks users to decode too much at once. The single biggest opportunity is to make graph semantics and density legible before adding more visual polish.

#### What's Working

- The domain legend and restrained blue/green/orange/violet palette give the graph an academic, controlled tone.
- Search, layout selection, filtering, fit, reset, and concept detail form a complete exploration loop.
- The right-side concept panel connects graph exploration to the canonical study page.

#### Priority Issues

- **[P1] Dense graph labels are unreadable at the default zoom:** 38 nodes and 75 edges produce small labels and overlapping relationships. This weakens the graph's primary job: orientation.
  - **Fix:** add an edge legend, show labels more selectively, and make selected-node neighborhood emphasis the default interaction pattern.
  - **Suggested command:** `$impeccable polish website/index.html`

- **[P1] Relationship semantics are under-explained:** Users see prerequisite and related filters, but no visible key explains arrows versus dashed lines.
  - **Fix:** add a compact relationship key beside the domain legend and a short selected-node explanation.
  - **Suggested command:** `$impeccable clarify website/index.html`

- **[P2] Filter state lacks recovery affordances:** A restrictive combination can leave little visible content without a clear “clear filters” path.
  - **Fix:** add active-filter count and group reset controls, plus an empty-state action that restores the graph.
  - **Suggested command:** `$impeccable harden website/index.html`

- **[P2] Scope is still cognitively expensive:** “Minimum scope (5 = broadest)” is better than importance, but the 1-5 scale is not explained in context.
  - **Fix:** add a compact scale cue or tooltip and avoid making the range the first filter users must interpret.
  - **Suggested command:** `$impeccable clarify website/index.html`

#### Persona Red Flags

**Alex (Power User):** No keyboard shortcut or fast filter reset. Repeated exploration requires several checkbox changes and manual zoom recovery.

**Jordan (First-Timer):** Cannot infer edge direction or node-size meaning from the initial screen. The graph looks like a colored network before it reads as a learning map.

#### Minor Observations

- The long domain and course lists consume substantial sidebar height.
- The statistics panel is more interpretable now, but relationship mix could use labels or visual swatches.
- Initial layout varies with force-directed positioning, which makes repeated comparison harder.

#### Questions to Consider

- Should the default view prioritize foundational nodes instead of showing every concept equally?
- Could the graph start with a selected concept or a small “atlas overview” mode?
- Would a compact edge legend reduce more confusion than adding more graph controls?
