const els = {
  title: document.getElementById("concept-title"),
  subtitle: document.getElementById("concept-subtitle"),
  meta: document.getElementById("concept-meta"),
  toc: document.getElementById("concept-toc"),
  article: document.getElementById("concept-article"),
  status: document.getElementById("concept-status"),
  rawLink: document.getElementById("raw-link"),
  breadcrumbTitle: document.getElementById("breadcrumb-title"),
  progressBar: document.getElementById("reading-progress-bar"),
};

const SECTION_ORDER = [
  "Definition",
  "Why it Matters",
  "Core Intuition",
  "How it Works",
  "Mathematical Foundation",
  "Key Components",
  "Advantages",
  "Limitations",
  "Common Mistakes",
  "Common Variants",
  "Real-world applications",
  "Interview Questions",
  "Related Concepts",
  "Connections",
  "Prerequisites",
  "Classification",
  "Contributing Courses",
  "Further Reading",
  "Slide-derived Evidence",
  "Provenance",
  "Extraction Metadata",
];

const SECTION_GROUPS = {
  Learn: new Set([
    "Definition",
    "Why it Matters",
    "Core Intuition",
    "How it Works",
    "Mathematical Foundation",
    "Key Components",
    "Advantages",
    "Limitations",
    "Common Mistakes",
  ]),
  Apply: new Set(["Common Variants", "Real-world applications", "Interview Questions"]),
  Connect: new Set(["Related Concepts", "Connections", "Prerequisites", "Classification", "Contributing Courses"]),
  Source: new Set(["Further Reading", "Slide-derived Evidence", "Provenance", "Extraction Metadata"]),
};

function slugify(text) {
  return String(text ?? "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function conceptNameFromPath(path) {
  const rawName = String(path ?? "").split("/").filter(Boolean).pop() || "Concept";
  try {
    return decodeURIComponent(rawName).replace(/\.md$/i, "") || "Concept";
  } catch {
    return rawName.replace(/\.md$/i, "") || "Concept";
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function inlineMarkdown(text) {
  let value = escapeHtml(text);
  value = value.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  value = value.replace(/`([^`]+)`/g, (_, code) => {
    const trimmed = code.trim();
    const looksMath =
      /\\[A-Za-z]+/.test(trimmed) ||
      /[\^_={}\[\]|+\-*/()]/.test(trimmed) ||
      /^p\(.+\|.+\)$/.test(trimmed);
    if (looksMath) {
      return `<span class="inline-math">\\(${escapeHtml(trimmed)}\\)</span>`;
    }
    return `<code>${escapeHtml(trimmed)}</code>`;
  });
  value = value.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
  return value;
}

function renderMathBlock(content) {
  const body = content.trim();
  if (!body) {
    return "";
  }
  return `<div class="math-block">\\[\n${escapeHtml(body)}\n\\]</div>`;
}

function loadMathJax() {
  if (window.MathJax?.typesetPromise) {
    return Promise.resolve(window.MathJax);
  }
  if (window.__mathJaxReady) {
    return window.__mathJaxReady;
  }

  window.__mathJaxReady = new Promise((resolve, reject) => {
    const script = document.querySelector('script[src*="mathjax"]');
    if (!script) {
      reject(new Error("MathJax script missing."));
      return;
    }
    script.addEventListener(
      "load",
      () => {
        const waitForStartup = window.MathJax?.startup?.promise ? window.MathJax.startup.promise : Promise.resolve();
        waitForStartup.then(() => resolve(window.MathJax)).catch(reject);
      },
      { once: true },
    );
    script.addEventListener("error", () => reject(new Error("Failed to load MathJax.")), { once: true });
  });

  return window.__mathJaxReady;
}

function parseFrontMatter(markdown) {
  const lines = markdown.split(/\r?\n/);
  if (lines[0] !== "---") {
    return { meta: {}, body: markdown };
  }
  const meta = {};
  let index = 1;
  while (index < lines.length && lines[index] !== "---") {
    const line = lines[index];
    const match = line.match(/^([A-Za-z0-9_ -]+):\s*(.*)$/);
    if (match) {
      let value = match[2].trim();
      value = value.replace(/^"(.*)"$/, "$1");
      meta[match[1].trim()] = value;
    }
    index += 1;
  }
  return { meta, body: lines.slice(index + 1).join("\n") };
}

function splitSections(markdown) {
  const lines = markdown.split(/\r?\n/);
  const sections = [];
  let title = "";
  let current = null;

  for (const line of lines) {
    if (line.startsWith("# ") && !title) {
      title = line.slice(2).trim();
      continue;
    }
    const match = line.match(/^##\s+(.*)$/);
    if (match) {
      current = { title: match[1].trim(), lines: [] };
      sections.push(current);
      continue;
    }
    if (current) {
      current.lines.push(line);
    }
  }

  return { title, sections };
}

function isTableRow(line) {
  return /^\|.*\|$/.test(line.trim());
}

function renderParagraph(text) {
  const content = text.trim();
  if (!content) {
    return "";
  }
  return `<p>${inlineMarkdown(content)}</p>`;
}

function renderList(items, ordered = false) {
  const tag = ordered ? "ol" : "ul";
  return `<${tag}>${items.map((item) => `<li>${inlineMarkdown(item)}</li>`).join("")}</${tag}>`;
}

function renderTable(rows) {
  if (!rows.length) {
    return "";
  }
  const header = rows[0];
  const body = rows.slice(1);
  return `
    <table>
      <thead><tr>${header.map((cell) => `<th>${inlineMarkdown(cell)}</th>`).join("")}</tr></thead>
      <tbody>
        ${body
          .map((row) => `<tr>${row.map((cell) => `<td>${inlineMarkdown(cell)}</td>`).join("")}</tr>`)
          .join("")}
      </tbody>
    </table>
  `;
}

function renderSectionContent(lines) {
  const chunks = [];
  let paragraph = [];
  let list = [];
  let ordered = false;
  let table = [];
  let inCode = false;
  let code = [];
  let inMath = false;
  let math = [];

  function flushParagraph() {
    if (paragraph.length) {
      chunks.push(renderParagraph(paragraph.join(" ")));
      paragraph = [];
    }
  }

  function flushList() {
    if (list.length) {
      chunks.push(renderList(list, ordered));
      list = [];
      ordered = false;
    }
  }

  function flushTable() {
    if (table.length) {
      const cleaned = table
        .filter((row) => row.some((cell) => cell.trim()))
        .map((row) => row.map((cell) => cell.trim()));
      if (cleaned.length) {
        const hasSeparator = cleaned.length > 1 && cleaned[1].every((cell) => /^-+$/.test(cell.replace(/:/g, "").trim()) || cell === "---");
        chunks.push(renderTable(hasSeparator ? [cleaned[0], ...cleaned.slice(2)] : cleaned));
      }
      table = [];
    }
  }

  function flushCode() {
    if (code.length) {
      chunks.push(`<pre><code>${escapeHtml(code.join("\n"))}</code></pre>`);
      code = [];
    }
  }

  function flushMath() {
    if (math.length) {
      chunks.push(renderMathBlock(math.join("\n")));
      math = [];
    }
  }

  for (const rawLine of lines) {
    const line = rawLine ?? "";
    const trimmed = line.trim();

    if (trimmed === "$$" || (trimmed.startsWith("$$") && trimmed.endsWith("$$") && trimmed.length > 4)) {
      if (inCode) {
        code.push(line);
        continue;
      }
      if (trimmed === "$$") {
        if (inMath) {
          flushMath();
          inMath = false;
        } else {
          flushParagraph();
          flushList();
          flushTable();
          inMath = true;
        }
        continue;
      }
      flushParagraph();
      flushList();
      flushTable();
      flushCode();
      chunks.push(renderMathBlock(trimmed.slice(2, -2)));
      continue;
    }

    if (trimmed.startsWith("```")) {
      if (inCode) {
        flushCode();
        inCode = false;
      } else {
        flushParagraph();
        flushList();
        flushTable();
        flushMath();
        inCode = true;
      }
      continue;
    }
    if (inCode) {
      code.push(line);
      continue;
    }
    if (inMath) {
      math.push(line);
      continue;
    }
    if (!line.trim()) {
      flushParagraph();
      flushList();
      flushTable();
      flushMath();
      continue;
    }
    if (/^(\d+)\.\s+/.test(trimmed)) {
      flushParagraph();
      flushTable();
      flushMath();
      if (!list.length) {
        ordered = true;
      }
      list.push(trimmed.replace(/^\d+\.\s+/, ""));
      continue;
    }
    if (/^[-*•]\s+/.test(trimmed)) {
      flushParagraph();
      flushTable();
      flushMath();
      if (!list.length) {
        ordered = false;
      }
      list.push(trimmed.replace(/^[-*•]\s+/, ""));
      continue;
    }
    if (isTableRow(line)) {
      flushParagraph();
      flushList();
      flushMath();
      table.push(line.split("|").slice(1, -1).map((cell) => cell.trim()));
      continue;
    }
    flushList();
    flushTable();
    if (/^#{3,6}\s+/.test(trimmed)) {
      flushMath();
      chunks.push(`<h3>${inlineMarkdown(trimmed.replace(/^#{3,6}\s+/, ""))}</h3>`);
      continue;
    }
    paragraph.push(trimmed);
  }

  flushParagraph();
  flushList();
  flushTable();
  flushMath();
  flushCode();

  return chunks.join("\n");
}

function renderToc(sections) {
  const groups = ["Learn", "Apply", "Connect", "Source"];
  els.toc.innerHTML = groups
    .map((group) => {
      const items = sections.filter((section) => SECTION_GROUPS[group].has(section.title));
      if (!items.length) return "";
      return `<div class="toc-group"><h3>${group}</h3>${items
        .map(
          (section) =>
            `<a class="toc-link" href="#section-${slugify(section.title)}">${escapeHtml(section.title)}</a>`,
        )
        .join("")}</div>`;
    })
    .join("");
}

function observeSections(sections) {
  if (!("IntersectionObserver" in window)) return;
  const links = new Map(
    [...els.toc.querySelectorAll(".toc-link")].map((link) => [link.getAttribute("href").slice(1), link]),
  );
  const firstLink = els.toc.querySelector(".toc-link");
  firstLink?.classList.add("is-active");
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (!visible.length) return;
      links.forEach((link) => link.classList.remove("is-active"));
      links.get(visible[0].target.id)?.classList.add("is-active");
    },
    { rootMargin: "-12% 0px -72% 0px", threshold: 0 },
  );
  sections.forEach((section) => {
    const element = document.getElementById(`section-${slugify(section.title)}`);
    if (element) observer.observe(element);
  });
}

function observeReadingProgress() {
  const update = () => {
    const pageHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = pageHeight > 0 ? Math.min(1, Math.max(0, window.scrollY / pageHeight)) : 0;
    els.progressBar.style.transform = `scaleX(${progress})`;
  };
  update();
  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
}

function renderMeta(meta) {
  const rows = [
    ["Domain", meta.domain || "Unknown"],
    ["Topic", meta.topic || "Unknown"],
    ["Type", meta.concept_type || "Unknown"],
    ["Scope", meta.scope_level ? `${meta.scope_level}/5` : "Unknown"],
    ["Study priority", meta.study_priority ? `${meta.study_priority}/5` : "Unknown"],
    ["Version", meta.version_number || "1"],
  ];
  els.meta.innerHTML = rows
    .map(([label, value]) => `<dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd>`)
    .join("");
}

function sectionSortKey(section) {
  const idx = SECTION_ORDER.indexOf(section.title);
  return idx >= 0 ? idx : SECTION_ORDER.length;
}

async function main() {
  const params = new URLSearchParams(window.location.search);
  const rawPath = params.get("path");
  if (!rawPath) {
    els.status.textContent = "Missing concept path.";
    return;
  }

  const pathConceptName = conceptNameFromPath(rawPath);
  document.title = pathConceptName;
  els.title.textContent = pathConceptName;
  els.breadcrumbTitle.textContent = pathConceptName;

  const markdownUrl = new URL(rawPath, window.location.href);
  els.rawLink.href = markdownUrl.href;

  const response = await fetch(markdownUrl);
  if (!response.ok) {
    els.status.textContent = `Unable to load concept page: ${response.status}`;
    return;
  }

  const markdown = await response.text();
  const { meta, body } = parseFrontMatter(markdown);
  const { title, sections } = splitSections(body);
  const orderedSections = [...sections].sort(
    (a, b) => sectionSortKey(a) - sectionSortKey(b) || a.title.localeCompare(b.title),
  );

  await loadMathJax().catch(() => null);

  const conceptName = title || meta.concept_name || "Concept";
  els.title.textContent = conceptName;
  document.title = conceptName;
  els.breadcrumbTitle.textContent = conceptName;
  els.subtitle.textContent = `${meta.domain || "Unknown domain"} · ${meta.topic || "Unknown topic"}`;
  renderMeta(meta);
  renderToc(orderedSections);

  els.status.hidden = true;
  els.article.innerHTML = "";

  orderedSections.forEach((section) => {
    const sectionEl = document.createElement("section");
    sectionEl.className = "concept-section";
    sectionEl.id = `section-${slugify(section.title)}`;
    sectionEl.innerHTML = `
      <h2>${escapeHtml(section.title)}</h2>
      ${renderSectionContent(section.lines)}
    `;
    els.article.appendChild(sectionEl);
  });

  observeSections(orderedSections);
  observeReadingProgress();

  if (window.MathJax?.typesetPromise) {
    await window.MathJax.typesetPromise([els.article]).catch(() => null);
  }
}

main().catch((error) => {
  els.status.textContent = `Failed to render concept page: ${error.message}`;
});
