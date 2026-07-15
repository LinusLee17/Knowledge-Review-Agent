---
name: Knowledge Review Agent
description: A calm, searchable study interface for consolidated university knowledge.
colors:
  bg: "#f4f6f9"
  surface: "#ffffff"
  surface-alt: "#eef2f7"
  border: "#d7dee8"
  ink: "#152033"
  muted: "#5c6b84"
  accent: "#315efb"
  accent-soft: "#e6ecff"
  machine-learning: "#2563eb"
  statistics: "#16a34a"
  business-analytics: "#f97316"
  data-science: "#8b5cf6"
  leadership: "#dc2626"
  communication: "#0ea5e9"
  digital-transformation: "#7c3aed"
  business: "#f59e0b"
  project-management: "#14b8a6"
  soft-skills: "#ef4444"
  other: "#64748b"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1.2
  title:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 700
    lineHeight: 1.25
  body:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  reading:
    fontFamily: "Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif"
    fontSize: "1.45rem"
    fontWeight: 600
    lineHeight: 1.2
  label:
    fontFamily: "Inter, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "0.8rem"
    fontWeight: 400
    lineHeight: 1.3
rounded:
  sm: "8px"
  md: "12px"
  pill: "999px"
spacing:
  xs: "0.35rem"
  sm: "0.5rem"
  md: "0.75rem"
  lg: "1rem"
  xl: "1.25rem"
components:
  button-default:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "0.6rem 0.85rem"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "1rem"
  input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "0.6rem 0.8rem"
---

# Design System: Knowledge Review Agent

## Overview

**Creative North Star: "The Concept Atlas"**

Knowledge Review Agent is a focused study tool. It should feel like an atlas of ideas: dependable, navigable, and quiet enough for sustained reading. The graph provides orientation, while concept pages provide the actual learning surface.

The interface uses an ink-and-paper study character through dark readable text, cool paper-like neutrals, restrained blue interaction states, and lightly layered white surfaces. Density is intentional, but hierarchy must keep the material scannable. Avoid cluttered dashboards, neon colors, unexplained metrics, and decoration that competes with the knowledge.

**Key Characteristics:**

- Calm, academic, and evidence-oriented.
- Dense but clearly structured.
- Lightly layered rather than heavily elevated.
- Color carries domain meaning and never acts as the only signal.

## Colors

The palette is an ink-and-paper neutral system with one interaction accent and a restrained set of domain colors.

### Primary

- **Atlas Blue** (`#315efb`): Focus rings, selected states, links, and primary interaction feedback.

### Secondary

- **Machine Learning Blue** (`#2563eb`): Machine Learning nodes.
- **Statistics Green** (`#16a34a`): Statistics nodes.
- **Business Analytics Orange** (`#f97316`): Business Analytics nodes.

### Tertiary

- **Data Science Violet** (`#8b5cf6`): Data Science nodes.
- **Communication Sky** (`#0ea5e9`): Communication nodes.
- **Project Teal** (`#14b8a6`): Project Management nodes.

### Neutral

- **Ink** (`#152033`): Primary text and headings.
- **Muted Ink** (`#5c6b84`): Supporting text, labels, and secondary metadata.
- **Cool Paper** (`#f4f6f9`): Page background.
- **Surface White** (`#ffffff`): Panels, controls, and reading surfaces.
- **Surface Alt** (`#eef2f7`): Chips, table headers, and secondary surfaces.
- **Atlas Border** (`#d7dee8`): Dividers and control borders.

### Named Rules

**The Ink-and-Paper Rule.** Keep reading surfaces light and text dark. Do not use neon accents or low-contrast gray text for primary content.

**The Domain Signal Rule.** Domain color supports labels and graph nodes, but meaning must remain available through text, shape, or position.

## Typography

**Display Font:** Iowan Old Style, Palatino Linotype, Palatino, or Georgia.

**Body Font:** Inter with system-ui and platform sans-serif fallbacks.

**Character:** UI controls stay in Inter for familiarity. Reading headings and concept titles use a restrained serif to create the feeling of an annotated atlas or study text without becoming ornamental.

### Hierarchy

- **Display** (700, 1.35rem, 1.2): Concept and page titles.
- **Reading** (600, 1.45rem, 1.2): Concept section headings and core intuition.
- **Title** (700, 1.2rem, 1.25): Graph page heading and panel titles.
- **Body** (400, 1rem, 1.55): Reading content and explanatory text.
- **Label** (400, 0.8rem, 1.3): Form labels, metadata, and supporting controls.

**The Study-Length Rule.** Keep explanatory text readable at roughly 65-75 characters per line where layout permits. Use density for metadata and controls, not for core explanations.

## Elevation

The system uses light tonal layering with restrained borders. Panels are primarily separated by surface color and a 1px border. Shadows appear only for transient overlays such as tooltips and search results.

### Shadow Vocabulary

- **Overlay shadow** (`0 10px 28px rgba(16, 24, 40, 0.08)`): Tooltips and search result popovers.
- **Resting surface** (`none`): Panels, graph stage, and concept article use borders and tonal contrast instead.

**The Quiet Surface Rule.** Resting content should not float dramatically. Use elevation to clarify temporary overlays, not to decorate every section.

## Components

### Buttons

- **Shape:** 10-12px radius, 1px border, 0.6rem x 0.85rem internal padding.
- **Default:** White surface with ink text and atlas border.
- **Hover:** Border darkens slightly; no decorative lift.
- **Focus:** 2px atlas-blue outline with 2px offset.

### Chips

- **Style:** Surface-alt background, ink text, pill radius, compact 0.28rem × 0.55rem padding.
- **State:** Use for concept metadata such as domain, topic, scope, and study priority.

### Cards / Containers

- **Corner Style:** 12px for panels and reading surfaces.
- **Background:** Surface white over cool paper.
- **Border:** 1px atlas border.
- **Internal Padding:** 1rem, with 1.25rem for larger reading headers.

### Inputs / Fields

- **Style:** White surface, 1px atlas border, 10px radius, minimum 2.6rem height.
- **Focus:** Atlas-blue outline, never color alone.
- **Disabled / Error:** Preserve readable text contrast and provide explicit state text where needed.

### Navigation

- **Graph page:** Top bar with search, layout, fit, and reset controls; sidebars hold filters and selected concept detail.
- **Concept page:** Header links return to the graph or open raw Markdown; sticky section navigation supports long-form study.
- **Mobile:** Collapse multi-column layouts into a single readable column without horizontal scrolling.

### Graph Nodes

- Domain color identifies subject area.
- Node size reflects structural scope, not subjective study value.
- Selection and search use borders and adjacency highlighting in addition to color.

### Graph Legend and Empty State

- **Legend:** Domain swatches sit above a compact relationship key. Prerequisites use a solid atlas-blue line with an arrow marker; related concepts use a dashed muted line.
- **Empty state:** When filters hide every node, use a centered white surface with a direct Clear filters action.

### Study Outline

- **Groups:** The concept-page TOC groups sections into Learn, Apply, Connect, and Source.
- **Active state:** The current section uses atlas-soft background and atlas-blue text, with the same meaning preserved for keyboard and pointer users.

## Do's and Don'ts

### Do:

- **Do** use the ink, cool paper, surface white, and atlas border tokens consistently.
- **Do** keep graph controls dense but labels explicit.
- **Do** make provenance and relationships available without interrupting the primary learning flow.
- **Do** preserve keyboard focus, readable contrast, responsive reflow, and reduced-motion behavior.
- **Do** use domain colors as supporting signals, never as the only source of meaning.

### Don't:

- **Don't** build cluttered dashboards or add unexplained metrics.
- **Don't** use neon colors, decorative gradients, or visual effects that compete with study content.
- **Don't** use large shadows on resting panels.
- **Don't** rely on color alone for domain or relationship meaning.
- **Don't** let presentation refinement alter technical content, equations, citations, or provenance.
