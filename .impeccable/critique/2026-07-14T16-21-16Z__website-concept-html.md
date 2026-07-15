---
target: website/concept.html
total_score: 32
p0_count: 0
p1_count: 1
timestamp: 2026-07-14T16-21-16Z
slug: website-concept-html
---
#### Design Health Score

| # | Heuristic | Score | Key Issue |
|---|---|---:|---|
| 1 | Visibility of System Status | 3 | Loading state and metadata are visible; long-page position is less clear. |
| 2 | Match System / Real World | 4 | Study-flow sections and source links match the learner's mental model. |
| 3 | User Control and Freedom | 3 | Back and raw-source links work; section navigation lacks a clear active state. |
| 4 | Consistency and Standards | 4 | Typography, panels, spacing, and controls align with the graph page. |
| 5 | Error Prevention | 3 | Missing content has fallbacks, but malformed source paths are not explained deeply. |
| 6 | Recognition Rather Than Recall | 4 | TOC, overview metadata, headings, tables, and math make the page scannable. |
| 7 | Flexibility and Efficiency | 3 | TOC supports fast navigation, but the 19-section list is long. |
| 8 | Aesthetic and Minimalist Design | 3 | Calm and readable, but metadata and provenance still compete with study content. |
| 9 | Error Recovery | 3 | Loading failures are surfaced, but recovery actions are limited. |
| 10 | Help and Documentation | 2 | Provenance is present, but unfamiliar fields such as scope and extraction metadata need plain-language cues. |
| **Total** | | **32/40** | Strong study page; focus polish on hierarchy and long-page navigation. |

#### Anti-Patterns Verdict

**LLM assessment:** The page feels deliberate and study-oriented, not strongly AI-generated. Its main risk is documentation-tool density: many operational sections are exposed with equal visual weight.

**Deterministic scan:** Clean. `detect.mjs --json website/concept.html` returned no findings.

**Browser evidence:** Gradient Descent renders with 19 sections, four MathJax containers, no horizontal overflow, and working raw Markdown access. No console errors or warnings appeared.

#### Overall Impression

This is already a credible revision page. The content order is substantially better than a raw pipeline record, but the top of the page still spends too much attention on classification before answering why the concept matters.

#### What's Working

- Definition, Why it Matters, Core Intuition, and How it Works create a strong learning sequence.
- Sticky overview and section navigation support both quick scanning and deep reading.
- Equations, symbol tables, source evidence, and provenance coexist without losing technical traceability.

#### Priority Issues

- **[P1] Study content starts below operational classification:** Classification and contributing courses appear before Definition, so the first reading moment is metadata rather than understanding.
  - **Fix:** keep a compact classification strip, but move detailed scope, priority, version, and provenance lower or collapse them.
  - **Suggested command:** `$impeccable polish website/concept.html`

- **[P2] The 19-section TOC is a long ungrouped list:** It is useful but visually flat and hard to scan on smaller screens.
  - **Fix:** group sections into Learn, Apply, Connect, and Source; keep provenance sections visually secondary.
  - **Suggested command:** `$impeccable layout website/concept.html`

- **[P2] Section position is not persistent:** Long reading has no progress cue or active TOC state.
  - **Fix:** highlight the current section and provide a restrained progress indicator that respects reduced motion.
  - **Suggested command:** `$impeccable polish website/concept.html`

- **[P3] Provenance and extraction metadata are visually similar to learning sections:** Traceability is valuable, but it should be discoverable without interrupting revision flow.
  - **Fix:** use a distinct source block treatment near the bottom with explicit “Source material” language.
  - **Suggested command:** `$impeccable clarify website/concept.html`

#### Persona Red Flags

**Alex (Power User):** Long TOC requires scanning; no active-section marker makes back-and-forth interview revision slower.

**Jordan (First-Timer):** “Scope”, “study priority”, and “extraction metadata” may look like required study concepts instead of repository metadata.

#### Minor Observations

- Raw Markdown is useful for debugging but should remain clearly secondary to the rendered page.
- Math rendering is correct in the inspected concept.
- The concept header could make the return-to-graph action more prominent on mobile.

#### Questions to Consider

- Should a learner see Definition before any provenance or classification detail?
- Can the TOC behave more like a study outline than a flat generated section list?
- Which metadata deserves to be visible by default during revision?
