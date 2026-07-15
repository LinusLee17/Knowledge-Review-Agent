"""Build the editable Knowledge Review Agent overview diagram."""

from __future__ import annotations

import json
import time
from pathlib import Path


OUT = Path(__file__).resolve().parents[1] / "outputs" / "Knowledge-Review-Agent-overview.excalidraw"
BG = "#f4f6f9"
INK = "#152033"
MUTED = "#5c6b84"
BORDER = "#d7dee8"
WHITE = "#ffffff"
BLUE = "#315efb"
BLUE_SOFT = "#e6ecff"
VIOLET = "#7048e8"
VIOLET_SOFT = "#f3eeff"
GREEN = "#16834a"
GREEN_SOFT = "#eaf8ef"
ORANGE = "#d97706"
ORANGE_SOFT = "#fff7e6"
RED = "#c2414b"
RED_SOFT = "#fff1f2"

elements: list[dict] = []
counter = 0


def eid(prefix: str) -> str:
    global counter
    counter += 1
    return f"{prefix}-{counter:03d}"


def base(kind: str, x: float, y: float, w: float, h: float, stroke: str = BORDER,
         fill: str = "transparent", width: float = 1.5) -> dict:
    now = int(time.time() * 1000)
    return {
        "id": eid(kind),
        "type": kind,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": stroke,
        "backgroundColor": fill,
        "fillStyle": "solid",
        "strokeWidth": width,
        "strokeStyle": "solid",
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "index": f"{counter:06d}",
        "roundness": {"type": 3} if kind == "rectangle" else None,
        "seed": 1000 + counter,
        "version": 1,
        "versionNonce": 2000 + counter,
        "isDeleted": False,
        "boundElements": None,
        "updated": now,
        "link": None,
        "locked": False,
    }


def rect(x: float, y: float, w: float, h: float, fill: str = WHITE,
         stroke: str = BORDER, width: float = 1.5) -> None:
    elements.append(base("rectangle", x, y, w, h, stroke, fill, width))


def text(value: str, x: float, y: float, w: float, h: float, size: float = 20,
         color: str = INK, bold: bool = False, align: str = "left") -> None:
    item = base("text", x, y, w, h, "transparent", "transparent", 0)
    item.update({
        "text": value,
        "originalText": value,
        "fontSize": size,
        "fontFamily": 5,
        "textAlign": align,
        "verticalAlign": "top",
        "containerId": None,
        "autoResize": False,
        "lineHeight": 1.25,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "isText": True,
        "fontStyle": "bold" if bold else "normal",
    })
    elements.append(item)


def arrow(x: float, y: float, dx: float, dy: float, color: str = BLUE) -> None:
    item = base("arrow", x, y, dx, dy, color, "transparent", 2)
    item.update({
        "points": [[0, 0], [dx, dy]],
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "roundness": {"type": 2},
    })
    elements.append(item)


def panel(x: float, y: float, w: float, h: float, label: str, fill: str) -> None:
    rect(x, y, w, h, fill, BORDER, 1.5)
    text(label, x + 28, y + 22, w - 56, 30, 18, BLUE, True)


# Canvas title.
text("Knowledge Review Agent", 80, 42, 1500, 48, 36, INK, True)
text("From scattered lecture notes to a living, interview-ready knowledge system", 82, 96, 1800, 30, 19, MUTED)

# 01 Context and problem.
panel(80, 166, 1040, 270, "01  CONTEXT + PROBLEM", "#f7f8fa")
text("University knowledge is scattered, long, and easy to forget.", 110, 220, 960, 52, 25, INK, True)
text(
    "Coming to the end of university, many courses and lecture notes have accumulated.\n"
    "Lecture packs can run hundreds of pages; important ideas fade after exams.\n"
    "Different courses often teach the same concept in different language.\n\n"
    "Need: fast, reliable review of concepts worth keeping for interviews and future work.",
    110, 286, 960, 120, 18, MUTED,
)

# 02 Solution.
panel(1160, 166, 1160, 270, "02  SOLUTION", BLUE_SOFT)
text("One coherent repository. One canonical page per concept.", 1190, 220, 1100, 52, 25, INK, True)
text(
    "Lecture material  ->  canonical concepts  ->  connected repository\n\n"
    "Cross-course overlap becomes an advantage instead of duplication.\n"
    "Example: Linear Regression appears once, with evidence from every contributing course.\n\n"
    "Result: a smaller, more useful knowledge surface than a larger slide archive.",
    1190, 286, 1100, 120, 18, MUTED,
)

# 03 Development flow: architecture diagram.
panel(80, 470, 2240, 360, "03  DEVELOPMENT FLOW  |  ARCHITECTURE", WHITE)
text("The flow separates knowledge generation from presentation.", 110, 516, 2100, 32, 23, INK, True)

stages = [
    ("Raw PDFs", "source material", WHITE, INK),
    ("Anthropic PDF Skill", "parse only", BLUE_SOFT, BLUE),
    ("Concept Filter", "curate concepts", VIOLET_SOFT, VIOLET),
    ("Knowledge\nConsolidator", "merge across courses", VIOLET_SOFT, VIOLET),
    ("Evaluation\nGate", "quality before polish", GREEN_SOFT, GREEN),
    ("Impeccable\nRefinement", "presentation only", BLUE_SOFT, BLUE),
    ("Knowledge Base\n+ Website", "readable output", WHITE, INK),
]
start_x, box_y, box_w, box_h, gap = 120, 594, 260, 112, 32
for i, (label, detail, fill, color) in enumerate(stages):
    x = start_x + i * (box_w + gap)
    rect(x, box_y, box_w, box_h, fill, color, 2)
    text(label, x + 18, box_y + 20, box_w - 36, 56, 20, color, True, "center")
    text(detail, x + 18, box_y + 77, box_w - 36, 24, 15, MUTED, False, "center")
    if i < len(stages) - 1:
        arrow(x + box_w + 8, box_y + box_h / 2, gap - 16, 0, BLUE)

text(
    "Each stage has one job. New or changed PDFs move incrementally. Evaluation runs before presentation refinement,\n"
    "so visual polish cannot hide knowledge-quality problems.",
    120, 748, 2160, 56, 17, MUTED,
)

# 04 Skills 1-3: the main focus.
panel(80, 870, 2240, 448, "04  SKILL FOCUS  |  THE CORE KNOWLEDGE WORK", "#fbfcfe")
text("Three focused Skills turn lecture material into durable knowledge.", 110, 916, 2100, 34, 23, INK, True)

skill_xs = [120, 850, 1580]
skill_data = [
    (
        "SKILL 1  |  CONCEPT FILTER", BLUE, BLUE_SOFT,
        "Filters slide noise\nExtracts durable concepts\nKeeps page-level provenance\n\nOutput\nlecture.md + lecture.json",
    ),
    (
        "SKILL 2  |  KNOWLEDGE CONSOLIDATOR", VIOLET, VIOLET_SOFT,
        "Deduplicates across courses\nSynthesizes one explanation\nMerges provenance and aliases\n\nOutput\nconcept.md + metadata.json",
    ),
    (
        "SKILL 3  |  KNOWLEDGE GRAPH BUILDER", GREEN, GREEN_SOFT,
        "Normalizes relationships\nConnects prerequisites\nUpdates incrementally\n\nOutput\ngraph.json",
    ),
]
for x, (label, color, fill, body) in zip(skill_xs, skill_data):
    rect(x, 970, 650, 300, fill, color, 2)
    text(label, x + 24, 998, 602, 40, 19, color, True)
    text(body, x + 24, 1054, 602, 190, 18, INK)

# 05 Issues and future improvements. Live demo intentionally omitted.
panel(80, 1358, 1100, 190, "05  ISSUES", RED_SOFT)
text(
    "PDF layouts and OCR can distort equations, tables, and diagrams.\n"
    "Conservative filtering trades recall for precision.\n"
    "Alias and relationship normalization still need review.",
    110, 1410, 1035, 108, 18, INK,
)
panel(1220, 1358, 1100, 190, "FUTURE IMPROVEMENTS", BLUE_SOFT)
text(
    "Improve extraction across varied course domains.\n"
    "Add human review for uncertain concepts.\n"
    "Extend website navigation and evaluation coverage.\n\n"
    "A living knowledge system, not a slide archive.",
    1250, 1410, 1035, 118, 18, INK,
)


doc = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "viewBackgroundColor": BG,
        "gridSize": 20,
        "gridStep": 5,
        "showGrid": False,
        "zoom": {"value": 0.72},
    },
    "files": {},
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {OUT} ({len(elements)} elements)")
