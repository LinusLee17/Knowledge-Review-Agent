import { resolveConceptPath } from './graph-contract.mjs?v=2';
import { escapeHtml, parseFrontMatter, splitSections, renderSectionContent } from './concept-markdown.mjs?v=3';

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

  const markdownUrl = resolveConceptPath(rawPath, {
    baseUrl: window.location.href,
    repoRootUrl: document.documentElement.dataset.repoRootUrl || undefined,
    refinedRootUrl: document.documentElement.dataset.refinedRootUrl || undefined,
  });
  els.rawLink.href = markdownUrl.href;

  const response = await fetch(markdownUrl);
  if (!response.ok) {
    els.status.textContent = `Unable to load concept page: ${response.status}`;
    return;
  }

  const markdown = await response.text();
  const { meta, body } = parseFrontMatter(markdown);
  const { title, preamble, sections } = splitSections(body);
  const contentBaseUrl = response.url || markdownUrl.href;
  const repoRootUrl = new URL(document.documentElement.dataset.repoRootUrl || '../', window.location.href);
  if (!repoRootUrl.pathname.endsWith('/')) repoRootUrl.pathname += '/';
  const markdownOptions = { legacySourceRootUrl: new URL('data/raw/', repoRootUrl).href };
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

  const prefixHtml = renderSectionContent(preamble, contentBaseUrl, markdownOptions);
  if (prefixHtml) {
    const prefixEl = document.createElement("section");
    prefixEl.className = "concept-section";
    prefixEl.innerHTML = prefixHtml;
    els.article.appendChild(prefixEl);
  }

  orderedSections.forEach((section) => {
    const sectionEl = document.createElement("section");
    sectionEl.className = "concept-section";
    sectionEl.id = `section-${slugify(section.title)}`;
    sectionEl.innerHTML = `
      <h2>${escapeHtml(section.title)}</h2>
      ${renderSectionContent(section.lines, contentBaseUrl, markdownOptions)}
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
